import timeit
import xml.sax
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from collections import defaultdict
from Stemmer import Stemmer
import re 

stop_words_dict= defaultdict(int)
title_dict = defaultdict(str)
pattern = re.compile("[^a-zA-Z0-9]")
title_index = defaultdict(list)

def build_stopWordsDict():                               # Building Stop Words Dictionary
    global stop_words_dict
    with open ('StopWords.txt','r') as f:
        for i in f:
            i=i.strip(' ').strip("\n")
            stop_words_dict[i]=1

def stem(datalist):                                        #Stemming the data
    finalLis=[]
    stemmer=Stemmer("english")
    for i in datalist:
        finalLis.append(stemmer.stemWord(i))
    return finalLis

def titleWrite(file_count):
    global title_dict
    with open("temp/title"+str(file_count)+".tsv","w") as f:
        li=sorted(title_dict.keys())
        fp.write(str(li[0]))
        for doc_id in (li):
            f.write(str(doc_id))
            f.write("\t"+str(title_dict[doc_id])+"\n")


def store_title_index(title_tag_words, page_count):
    global title_index
    index = str(page_count)
    for word in title_tag_words :
        s = index + ":" + str(title_tag_words[word])
        title_index[word].append(s)


class WikiHandler(xml.sax.ContentHandler):
    title_file_count = 0
    def __init__(self):
        self.title=0
        self.title_data = ""
        self.page_count = 0 # For Counting the pages Parsed till now
        self.title_count = 0 # Counting title for 1 title file
        self.title_file_count = 0
        self.title_id_stat = 0
        self.page_stat = 0
        self.bufid = "" # For Unique ID of Title 
        self.title_tag_words = dict() # For Storing the Title Tag Words

    
    
    def Index_Create_Fun(self):
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
            self.title_tag_words = dict() # Making the Title tag dictionary as empty for every page
        

    def characters(self, content):
        if (self.title_id_stat==1 and self.page_stat==1):
            self.bufid += content
            title_dict[int(self.bufid)]=self.title_data
        if(self.title == 1):
            self.title_data += content


            # Adding title content to the dictionary
            title_text = content
            title_text = title_text.lower()
            global pattern
            title_text = re.split(pattern, title_text)
            for word in title_text:
                if word:
                    if word not in stop_words_dict:
                        if word not in self.title_tag_words:
                            self.title_tag_words[word] = 1
                        else:
                            self.title_tag_words[word] += 1

    def endElement(self, tag):
        if(tag=="page"):
            self.page_stat=0
            self.title_count+=1            
        if(tag=="id"):
            self.title_id_stat=0
        if(tag == "title"):
            self.title = 0
            store_title_index(self.title_tag_words, self.page_count)
        if(tag=="text"):
            WikiHandler.Index_Create_Fun(self)
        
            


def main():
    global fp, title_index

    fp=open("temp/title_offset.tsv","w")
    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse('tiny.xml')
    titleWrite(WikiHandler.title_file_count)

    print(title_index)


if __name__ == "__main__":                                          
    start = timeit.default_timer()
    build_stopWordsDict()
    main()
    stop = timeit.default_timer()
    print (stop - start)
