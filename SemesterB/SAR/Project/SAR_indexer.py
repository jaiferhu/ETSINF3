import sys
import os
import pickle
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer

def process(s):
    #Delete non alphanumerical characters
    for character in s:
        if not character.isalpha():
            s=s.replace(character, ' ')
    s=s.lower()
    return s

def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def stemList(z,stemmer):
    diccStem={}
    for term in z:
        resul=stemmer.stem(term)
        l = diccStem.get(resul, [])
        l.append(term)
        diccStem[resul] = l
    return diccStem


def unionor(list1, list2):
    c = []
    jj = 0
    kk = 0
    list1 = sorted(list1)
    list2 = sorted(list2)
    while jj < len(list1) and kk < len(list2):
        if list1[jj] == list2[kk]:
            c.append(list1[jj])
            jj += 1
            kk += 1
        else:
            if list1[jj][0] < list2[kk][0]:
                c.append(list1[jj])
                jj += 1
            elif list1[jj][0] == list2[kk][0]:
                if list1[jj][1] < list2[kk][1]:
                    c.append(list1[jj])
                    jj += 1
                else:
                    c.append(list2[kk])
                    kk += 1
            else:
                c.append(list2[kk])
                kk += 1
    while jj < len(list1):
        c.append(list1[jj])
        jj += 1
    while kk < len(list2):
        c.append(list2[kk])
        kk += 1

    return c


def main():
    print('Starting indexation')
    direc=sys.argv[1]
    dictDoc={}
    postingListTE={}
    postingListTI={}
    postingListCA={}
    postingListDA={}
    postingListStemTE={}
    postingListStemTI = {}
    postingListStemCA = {}
    postingListStemDA = {}
    finalName=sys.argv[2]
    docid=0
    diccT={}
    buffer=[]
    stemmer = SnowballStemmer('spanish')
    for filename in sorted(os.listdir(direc)):
        diccT[docid]=direc+'/'+filename
        docid+=1
        print('Indexing file: '+direc+'/'+filename)
        dictDoc[filename]=docid
        aux=open(direc+'/'+filename,'r')
        raw=aux.read()
        rawlist=raw.split('<DOC>')
        nnew=0
        for new in range(1,len(rawlist)):
            nnew+=1
            newid=(docid,nnew)
            buffer.append(list(newid))
            #TEXT dicc
            Nrawtext=rawlist[new][rawlist[new].find('<TEXT>')+len('<TEXT>'):rawlist[new].find('</TEXT>')]
            Ntext=process(Nrawtext)
            z = Ntext.split()
            for term in set(z):
                l = postingListTE.get(term, [])
                l.append(newid)
                postingListTE[term] = l

            #Title dicc
            Nrawtext=rawlist[new][rawlist[new].find('<TITLE>') + len('<TITLE>'):rawlist[new].find('</TITLE>')]
            Ntext = process(Nrawtext)
            z = Ntext.split()
            for term in set(z):

                l = postingListTI.get(term, [])
                l.append(newid)
                postingListTI[term] = l

            #Category dicc
            Nrawtext =rawlist[new][rawlist[new].find('<CATEGORY>') + len('<CATEGORY>'):rawlist[new].find('</CATEGORY>')]
            Ntext = process(Nrawtext)
            z = Ntext.split()
            for term in set(z):
                l = postingListCA.get(term, [])
                l.append(newid)
                postingListCA[term] = l

            #Date dicc
            Nrawtext =rawlist[new][rawlist[new].find('<DATE>') + len('<DATE>'):rawlist[new].find('</DATE>')]
            z = Nrawtext.split()
            for term in set(z):
                l = postingListDA.get(term, [])
                l.append(newid)
                postingListDA[term] = l


        aux.close()


    print(len(buffer))
    print("Stemming...  ")
    print("1")

    print(2)
    #sys.exit()

    #Stemming text
    keys = list(postingListTE.keys())
    stemmingDiccTE = stemList(keys, stemmer)
    for k in stemmingDiccTE:
        newPL=[]
        for w in stemmingDiccTE[k]:
            newPL=unionor(newPL,postingListTE[w])
        for ww in stemmingDiccTE[k]:
            postingListStemTE[ww] = newPL
    print(len(postingListStemTE))
    print("Text stemmed")

    # Stemming title
    keys = list(postingListTI.keys())
    stemmingDiccTI = stemList(keys, stemmer)
    for k in stemmingDiccTI:
        newPL = []
        for w in stemmingDiccTI[k]:
            newPL = unionor(newPL, postingListTI[w])
        for ww in stemmingDiccTI[k]:
            postingListStemTI[ww] = newPL
    print("Titles stemmed")

    # Stemming category
    keys = list(postingListCA.keys())
    stemmingDiccCA = stemList(keys, stemmer)
    for k in stemmingDiccCA:
        newPL = []
        for w in stemmingDiccCA[k]:
            newPL = unionor(newPL, postingListCA[w])
        for ww in stemmingDiccCA[k]:
            postingListStemCA[ww] = newPL
    print("Categories stemmed")

    print("Done")
    postingListRE=(postingListTE,postingListTI,postingListCA,postingListDA)
    postingListStemRE=(postingListStemTE,postingListStemTI,postingListStemCA,postingListDA)
    save_object( ( postingListRE, postingListStemRE ,diccT,buffer),finalName)
    sys.exit()

main()
