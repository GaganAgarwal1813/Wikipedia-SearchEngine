import timeit
from unicodedata import category
import xml.sax
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from collections import defaultdict
# from Stemmer import Stemmer
import pickle
import re 

stop_words_dict= defaultdict(int)
title_dict = defaultdict(str)
pattern = re.compile("[^a-zA-Z0-9]")
# RE to remove urls
regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
# RE to remove tags & css
regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
title_pos = list() # Which title is present at which location in the file
title_index = defaultdict(list)
body_index = defaultdict(list)
category_index = defaultdict(list)
info_box_index = defaultdict(list)
word_position = dict()


def preprocess(word):
    word = word.strip()
    word = word.lower()
    stemmer = nltk.stem.SnowballStemmer('english')
    word = stemmer.stem(word)
    return word


def build_stopWordsDict():                               # Building Stop Words Dictionary
    global stop_words_dict
    with open ('StopWords.txt','r') as f:
        for i in f:
            i=i.strip(' ').strip("\n")
            stop_words_dict[i]=1


def titleWrite(file_count):
    global title_dict, title_pos
    with open("temp/title"+str(file_count)+".txt","w") as f:
        # li=sorted(title_dict.keys())
        # fp.write(str(li[0]))
        for value in (title_dict.values()):
            title_pos.append(f.tell())
            f.write(str(value)+"\n")
            
            # f.write("\t"+str(title_dict[doc_id])+"\n")

def title_pos_pickle_write():
    global title_pos
    file = open("temp/title_pos.pickle", "wb+")
    pickle.dump(title_pos, file)
    file.close()

def title_word_loc_write(file_count):
    global title_index
    global word_position
    fptr=0
    file = "temp/tword_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in title_index:
        index = ",".join(title_index[word])+"\n"
        outfile.write(index)
        if word in word_position :
            word_position[word]['t']=fptr
        else:
            word_position[word] = {}
            word_position[word]['t']=fptr
        fptr = fptr + len(index)
    outfile.close()

    
def body_word_loc_write(file_count):
    global body_index, word_position
    
    fptr=0
    file = "temp/bword_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in body_index:
        index = ",".join(body_index[word])+"\n"
        outfile.write(index)
        if word in word_position :
            word_position[word]['b']=fptr
        else:
            word_position[word] = {}
            word_position[word]['b']=fptr
        fptr = fptr + len(index)
    outfile.close()


def category_word_loc_write(file_count):
    global category_index, word_position
    fptr=0
    file = "temp/cword_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in category_index:
        # print(word)
        index = ",".join(category_index[word])+"\n"
        # print(index)
        outfile.write(str(index))
        if word in word_position :
            word_position[word]['c']=fptr
        else:
            word_position[word] = {}
            word_position[word]['c']=fptr
        fptr = fptr + len(index)
    outfile.close()
    # print(word_position)

def info_box_loc_write(file_count):
    global info_box_index, word_position
    fptr=0
    file = "temp/info_box_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in info_box_index:
        index = ",".join(info_box_index[word])+"\n"
        outfile.write(index)
        if word in word_position :
            word_position[word]['i']=fptr
        else:
            word_position[word] = {}
            word_position[word]['i']=fptr
        fptr = fptr + len(index)
    outfile.close()

def store_title_index(title_tag_words, page_count):
    global title_index
    index = str(page_count)
    for word in title_tag_words :
        s = index + ":" + str(title_tag_words[word])
        title_index[word].append(s)

def store_body_index(body_tag_words, page_count):
    global body_index
    index = str(page_count)
    for word in body_tag_words :
        s = index + ":" + str(body_tag_words[word])
        body_index[word].append(s)

def store_category_index(category_tag_words, page_count):
    global category_index
    index = str(page_count)
    for word in category_tag_words :
        s = index + ":" + str(category_tag_words[word])
        category_index[word].append(s)
    # print(category_index)
def store_info_box_index(info_box_words, page_count):
    global info_box_index
    index = str(page_count)
    for word in info_box_words :
        s = index + ":" + str(info_box_words[word])
        info_box_index[word].append(s)


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
        self.body_words = dict() # For Storing the Body Words
        self.category_words = dict() # For Storing the Category Words
        self.info_box_words = dict()
        self.body_stat = 0

    
    
    def Index_Create_Fun(self):
        global title_dict
        global title_index
        if self.title_count > 20000000:
            # print(self.title_count)
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
            self.body_words = dict() # Making the Body dictionary as empty for every page
        if(tag == "text"):
            self.body_stat = 1
        

    def characters(self, content):
        global pattern, regExp1, regExp2
        if (self.title_id_stat==1 and self.page_stat==1):
            self.bufid += content
            title_dict[int(self.bufid)]=self.title_data
        if(self.title == 1):
            self.title_data += content
            # Adding title content to the dictionary
            title_text = content
            title_text = title_text.lower()
            
            title_text = re.split(pattern, title_text)
            for word in title_text:
                if word:
                    if word not in stop_words_dict and len(word)>2:
                        if word not in self.title_tag_words:
                            self.title_tag_words[word] = 1
                        else:
                            self.title_tag_words[word] += 1
        if(self.body_stat == 1):
            # global pattern
            stemmer = nltk.stem.SnowballStemmer('english')
            body_text = content
            body_text = regExp1.sub('',body_text)
            body_text = regExp2.sub('',body_text)

            temp_category_word = re.findall("\[\[Category:(.*?)\]\]", body_text)
            if temp_category_word:
                for w in temp_category_word:
                    w = re.split(pattern, w)
                    for word in w:
                        word = preprocess(word)
                        # print(word)
                        if word:
                            if word not in stop_words_dict and len(word)>2:
                                if word not in self.category_words:
                                    self.category_words[word] = 1
                                else:
                                    self.category_words[word] += 1
                
            temp_info_box_word = re.findall("{{Infobox((.|\n)*?)}}", body_text)
            if temp_info_box_word:
                for w in temp_info_box_word:
                    w = re.split(pattern, w)
                    for word in w:
                        word = preprocess(word)
                        if word:
                            if word not in stop_words_dict and len(word)>2:
                                if word not in self.info_box_words:
                                    self.info_box_words[word] = 1
                                else:
                                    self.info_box_words[word] += 1

            body_text = body_text.lower()
            body_text = re.split(pattern, body_text)
            for word in body_text:
                if word:
                    
                    word = stemmer.stem(word)
                    if word not in stop_words_dict and len(word)>2:
                        if word not in self.body_words:
                            self.body_words[word] = 1
                        else:
                            self.body_words[word] += 1

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
            self.body_stat=0
            store_body_index(self.body_words, self.page_count)
            # print(self.category_words)
            store_category_index(self.category_words, self.page_count)
            store_info_box_index(self.info_box_words, self.page_count)
            WikiHandler.Index_Create_Fun(self)
        
def dump_data_pickel():
    global word_position
    file = open("temp/wpos"+str(WikiHandler.title_file_count)+".pickle", "wb+")
    pickle.dump(word_position, file)
    file.close()         


def main():
    global fp, title_index, body_index

    fp=open("temp/title_offset.tsv","w")
    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse('tiny.xml')
    # Parsing Done
    # Writing Titles to File
    titleWrite(WikiHandler.title_file_count)
    # Writing Title Index to File
    title_word_loc_write(WikiHandler.title_file_count)
    # Writing Title Position to Pickle File
    title_pos_pickle_write()
    # Writing Body Index to File

    body_word_loc_write(WikiHandler.title_file_count)

    # Writing Category Index to File
    category_word_loc_write(WikiHandler.title_file_count)

    # writing Info-Box index to file
    info_box_loc_write(WikiHandler.title_file_count)

    dump_data_pickel()
    
    
    # print(body_index)

if __name__ == "__main__":                                          
    start = timeit.default_timer()
    build_stopWordsDict()
    main()
    stop = timeit.default_timer()
    print (stop - start)
