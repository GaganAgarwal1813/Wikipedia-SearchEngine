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
unique_words = set()

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

def removeStopWords(dataLis):                           # Removing Stop Words
    temp=[key for key in dataLis if stopwords[key]!=1]
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
    start = timeit.default_timer()
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]
    stop = timeit.default_timer()
    print ("fe "+str(stop - start))
    tokens = [re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) for text in tokens]
    return tokens


class WikiHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.body=0
        self.body_data = ""
        self.page_count = 0

    def startElement(self,tag,attr):
        global unique_words
        if(tag == "text"):
            self.body = 1
        if(tag == "page"):
            if(self.page_count == 10):
                print(unique_words)
                print(len(unique_words))
                exit()
            self.page_count = self.page_count+1

    def characters(self, content):
        global unique_words
        if(self.body == 1):
            self.body_data += content
            token = (preProcess(self.body_data)) 
            token = token[:int(len(token)*0.2)]
            unique_words.update(token)



    def endElement(self, tag):
        if(tag != "text"):
            self.body = 0



def main():
    global unique_words
    # fp=open("temp/title_offset","w")
    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse('data.xml')
    print("No of Unique words"+unique_words)



if __name__ == "__main__":                                          
    start = timeit.default_timer()
    build_stopWordsDict()
    main()
    stop = timeit.default_timer()
    print (stop - start)
