import timeit
import xml.sax
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag
from collections import defaultdict
from Stemmer import Stemmer
import re 

stopwords= defaultdict(int)
title_dict = defaultdict(str)

def build_stopWordsDict():                               # Building Stop Words Dictionary
    global stopwords
    with open ('StopWords.txt','r') as f:
        for i in f:
            i=i.strip(' ').strip("\n")
            stopwords[i]=1

def makeDict(datalist):
    datalist = removeStopWords(datalist)
    p=[]
    temp=defaultdict(int)
    datalist= stem(datalist)

    for x in datalist:
        temp[x]=temp[x]+1
    return temp

def preProcess(text):
    # Converting to lower case
    text = text.lower()
    # Removing all the special characters
    text_p = "".join([char for char in text if char not in string.punctuation])
    # Tokenizing the text
    tokens = word_tokenize(text_p)
    # Removing stop words
    tokens = removeStopWords(tokens)
    # Stemming the tokens
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]
    return tokens

def processTitle(data):
    data=data.lower()
    data_tok=re.findall(r'\d+|[\w]+',data)
    temp=makeDict(data_tok)
    return temp  

def removeStopWords(dataLis):                           # Removing Stop Words
    temp=[key for key in dataLis if stopwords[key]!=1]
    return temp

def stem(datalist):                                        #Stemming the data
    finalLis=[]
    stemmer=Stemmer("english")
    for i in datalist:
        finalLis.append(stemmer.stemWord(i))
    return finalLis

def titleWrite(file_count):
    global title_dict
    with open("temp/title"+str(file_count),"w") as f:
        li=sorted(title_dict.keys())
        fp.write(str(li[0]))
        for doc_id in (li):
            f.write(str(doc_id))
            f.write("-"+str(title_dict[doc_id])+"\n")


class WikiHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.title=0
        self.title_data = ""
        self.page_count = 0 # For Counting the pages Parsed till now
        self.title_count = 0 # Counting title for 1 title file
        self.title_file_count = 0
        self.title_id_stat = 0
        self.page_stat = 0
        self.bufid = "" # For Unique ID of Title 
    
    def Index_Create_Fun(self,title_data):
        global title_dict
        if self.title_count > 200000:
            print(self.title_count)
            titleWrite(self.title_file_count)
            self.title_count = 0
            self.title_file_count = self.title_file_count + 1
            title_dict=defaultdict(str)

    
    def startElement(self,tag,attr):
        if(tag=="id" and self.page_stat==0):
            self.page_stat=1
            self.title_id_stat=1
            self.bufid=""
        if(tag == "title"):
            self.title = 1
            self.title_data = ""
        if(tag == "page"):
            self.page_count = self.page_count + 1
            self.title_count = self.title_count + 1
        

    def characters(self, content):
        if (self.title_id_stat==1 and self.page_stat==1):
            self.bufid += content
            title_dict[int(self.bufid)]=self.title_data
        if(self.title == 1):
            self.title_data += content
        

    def endElement(self, tag):
        if(tag=="page"):
            self.page_stat=0
            self.title_count+=1
        if(tag=="id"):
            self.title_id_stat=0
        if(tag == "title"):
            self.title = 0
            self.title_data_dict = processTitle(self.title_data)
        if(tag=="text"):
            WikiHandler.Index_Create_Fun(self,self.title_data )
        
            


def main():
    global fp
    fp=open("temp/title_offset","w")
    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse('data.xml')



if __name__ == "__main__":                                          
    start = timeit.default_timer()
    build_stopWordsDict()
    main()
    stop = timeit.default_timer()
    print (stop - start)
