import timeit
import xml.sax
from Stemmer import Stemmer
from collections import defaultdict
import pickle
import re 
import sys
import os



dump_path = ""
index_path = ""
stemmer = Stemmer('porter')
stop_words_dict= defaultdict(int)
pattern = re.compile("[^a-zA-Z0-9]")
title_pos = list() # Which title is present at which location in the file
title_index = defaultdict(list)
body_index = defaultdict(list)
category_index = defaultdict(list)
info_box_index = defaultdict(list)
ext_links_index = defaultdict(list)
references_index = defaultdict(list)
word_position = dict()
external_link_words = dict()
category_tag_words = dict()
info_box_words = dict()
body_regex = re.compile("== ?[a-z]+ ?==\n(.*?)\n")
title_tags = ""
stemWordDict = dict()

token_count = 0


# For Preprocessing word and building a stemmer dictionary
def preprocessWord(word):
    global stemWordDict
    word = word.lower()
    word = word.strip()
    if word not in stemWordDict:
        stemWordDict[word] = stemmer.stemWord(word)
    return stemWordDict[word]

def remove_redundant_body(body):
    # Regex Remove URL
    regUrl = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
    body = regUrl.sub('', body)
    # Regex Remove HTML Tags CSS
    regHTML = re.compile(r'{\|(.*?)\|}',re.DOTALL)
    body = regHTML.sub('', body)
    # Regular Expression to remove {{cite **}} or {{vcite **}}
    regcite = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)
    body = regcite.sub('', body)
    # Regular Expression to remove [[file:]]
    regfile = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
    body = regfile.sub('', body)
    return body




def preprocess_word(word):
    word = word[:int(len(word)*0.6)]
    word = word.strip()
    return word


def build_stopWordsDict():                               # Building Stop Words Dictionary
    global stop_words_dict
    with open ('StopWords.txt','r') as f:
        for i in f:
            i=i.strip(' ').strip("\n")
            stop_words_dict[i]=1


def titleWrite(file_count, title_text):
    global title_pos, title_tags
    title_pos.append(title_tags.tell())
    title_tags.write(title_text)


def title_pos_pickle_write():
    global title_pos, index_path
    file = open(index_path + "/title_pos.pickle", "wb+")
    pickle.dump(title_pos, file)
    file.close()

def title_word_loc_write(file_count):
    global title_index, index_path
    global word_position
    fptr=0
    file = index_path + "/tword_idx"+str(file_count)+".txt"
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
    global body_index, word_position, index_path
    
    fptr=0
    file = index_path + "/bword_idx"+str(file_count)+".txt"
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
    global category_index, word_position, index_path
    fptr=0
    file = index_path + "/cword_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in category_index:
        index = ",".join(category_index[word])+"\n"
        if word in word_position :
            word_position[word]['c']=fptr
        else:
            word_position[word] = {}
            word_position[word]['c']=fptr
        outfile.write(str(index))
        fptr = fptr + len(index)
    outfile.close()

def info_box_loc_write(file_count):
    global info_box_index, word_position, index_path
    fptr=0
    file = index_path + "/info_box_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in info_box_index:
        index = ",".join(info_box_index[word])+"\n"
        if word in word_position :
            word_position[word]['i']=fptr
        else:
            word_position[word] = {}
            word_position[word]['i']=fptr
        outfile.write(index)
        fptr = fptr + len(index)
    outfile.close()

def references_loc_write(file_count):
    global references_index, word_position, index_path
    fptr = 0
    file = index_path + "/references_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in references_index:
        index = ",".join(references_index[word])+"\n"
        
        if word in word_position :
            word_position[word]['r']=fptr
        else:
            word_position[word] = {}
            word_position[word]['r']=fptr
        outfile.write(index)
        fptr = fptr + len(index)
    outfile.close()

def ext_link_loc_write(file_count):
    global ext_links_index, word_position, index_path
    fptr = 0
    file = index_path + "/ext_link_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in ext_links_index:
        index = ",".join(ext_links_index[word])+"\n"
        outfile.write(index)
        if word in word_position :
            word_position[word]['e']=fptr
        else:
            word_position[word] = {}
            word_position[word]['e']=fptr
        fptr = fptr + len(index)
    outfile.close()

def store_title_index(title_tag_words, page_count):
    global title_index
    index = str(page_count)
    for word in title_tag_words :
        s = index + ":" + str(title_tag_words[word])
        title_index[word].append(s)

def store_body_index(body_tag_words, page_count):
    global body_index, external_link_words, category_tag_words
    index = str(page_count)
    for word in body_tag_words :
        if(word not in external_link_words and word not in category_tag_words):
            s = index + ":" + str(body_tag_words[word])
            body_index[word].append(s)



def store_category_index(page_count):
    global category_index, category_tag_words
    index = str(page_count)
    for word in category_tag_words :
        s = index + ":" + str(category_tag_words[word])
        category_index[word].append(s)

def store_references(references_words, page_count):
    global references_index
    index = str(page_count)
    for word in references_words :
        s = index + ":" + str(references_words[word])
        references_index[word].append(s)

def store_info_box_index(page_count):
    global info_box_index, info_box_words
    index = str(page_count)
    for word in info_box_words :
        s = index + ":" + str(info_box_words[word])
        info_box_index[word].append(s)

def store_ext_links_index(ext_links, page_count):
    global ext_links_index
    index = str(page_count)
    for word in ext_links :
        s = index + ":" + str(ext_links[word])
        ext_links_index[word].append(s)


def external_link_process(ext_link_cont, page_count):
    links = ''
    global stemmer, external_link_words, token_count
    text = (ext_link_cont.split("==External links=="))
    if len(text)>1:
        text=text[1].split("\n")[1:]
        for txt in text:
            if txt=='':
                break
            if txt[0]=='*':
                # txt = stemmer.stem(txt)
                text_split=txt.split(' ')
                link=[wd for wd in text_split if 'http' not in wd]
                link=' '.join(link)
                links+=' '+link
    # external_link_words = dict()
    links = links.replace('\n', ' ').replace('File:', ' ')
    links = re.sub('(http://[^ ]+)', ' ', links)
    links = re.sub('(https://[^ ]+)', ' ', links)
    links = re.sub('\{.*?\}|\[.*?\]|\=\=.*?\=\=', ' ', links)
    links = ''.join([i if ord(i) < 128 else ' ' for i in links])
    links = ''.join(ch if ch.isalnum() else ' ' for ch in links)
    links = links.split()

    token_count += len(links)

    for word in links:
        if word:
            word = word.lower()
            if word not in stop_words_dict and len(word)>2 and len(word)<13:
                if word not in external_link_words:
                    external_link_words[word] = 1
                else:
                    external_link_words[word] += 1
    store_ext_links_index(external_link_words, page_count)


def tokenizeInfo(text):
    global stemmer, token_count
    text = re.split(r'[^A-Za-z0-9]+', text)
    token_count += len(text)
    tokens = []
    for word in text:
        word = stemmer.stemWord(word)
        if len(word) > 2 and len(word) < 13 and word not in stop_words_dict:
            tokens.append(word)
    return tokens


def extractCategories(text, page_count):
    cat = re.findall("\[\[Category:(.*?)\]\]", text)
    global category_tag_words
    for line in cat:
        words = re.split(pattern, line)
        for i in words:
            i = preprocessWord(i)
            if i and len(i) > 2 and i not in stop_words_dict:
                if i not in category_tag_words:
                    category_tag_words[i] = 1
                else:
                    category_tag_words[i] += 1

    store_category_index(page_count)


def processInfo(text, page_count):
    info_cont = re.findall(r"{{Infobox((.|\n)*?)}}", text)
    global info_box_words
    for line in info_cont:
        for i in line:
            i = re.split(pattern, i)
            for j in i:
                j = preprocessWord(j)
                if j and len(j) > 2 and j not in stop_words_dict:
                    if j not in info_box_words:
                        info_box_words[j] = 1
                    else:
                        info_box_words[j] += 1
    # print("info_box_words", info_box_words)
    store_info_box_index(page_count)

def refandextType(name):
	l = []
	l.append("==" + name + "==")
	l.append("== " + name + "==")		
	l.append("==" + name + " ==")		
	l.append("== " + name + " ==")		
	return l

def getReferences(text, page_count):
    ref = text.split("[[")
    ref = tokenizeInfo(ref[0])
    d = {}
    for i in ref:
        if i.isnumeric()==False:
            if i in d:
                d[i] +=1
            else:
                d[i] = 1
    store_references(d, page_count)

def processContent(text, page_count):
    text=text.lower()
    ref = refandextType("references")
    ext = refandextType("external links")
    data=text.split(ref[0])
    if data[0] == text:
        data= text.split(ref[1])
    if data[0]==text:
        data= text.split(ref[2])
    if data[0]==text:
        data= text.split(ref[3])
    if len(data)==1:
        # extractCategories(data[0], page_count)
        catdata=data[0].split(ext[0])
        if len(catdata)==1:
            catdata=data[0].split(ext[1])
        if len(catdata)==1:
            catdata=data[0].split(ext[2])
        if len(catdata)==1:
            catdata=data[0].split(ext[3])
    else:
        catdata=data[1].split(ext[0])
        if len(catdata)==1:
            catdata=data[1].split(ext[1])
        if len(catdata)==1:
            catdata=data[1].split(ext[2])
        if len(catdata)==1:
            catdata=data[1].split(ext[3])
        getReferences(data[1], page_count)
        # extractCategories(data[1], page_count)
    # processInfo(data[0], page_count)


class WikiHandler(xml.sax.ContentHandler):
    title_file_count = 0
    body_content = ""
    def __init__(self):
        self.title=0
        self.title_data = ""
        self.page_count = 0 # For Counting the pages Parsed till now
        self.title_file_count = 0
        self.title_tag_words = dict() # For Storing the Title Tag Words
        self.category_words = dict() # For Storing the Category Words
        self.body_stat = 0
        self.body_content = ""
        self.body_words = dict() # For Storing the Body Words

    
    def startElement(self,tag,attr):
        if(tag == "title"):
            self.title = 1
            self.title_data = ""
        if(tag == "page"):
            self.page_count = self.page_count + 1
            self.title_tag_words = dict() # Making the Title tag dictionary as empty for every page
        if(tag == "text"):
            self.body_stat = 1
            self.body_words = dict()
        

    def characters(self, content):
        global pattern, title_pos, token_count
        if(self.title == 1):
            self.title_data += content
            # Adding title content to the dictionary
            
        if(self.body_stat == 1):
            self.body_content += content
           
    def endElement(self, tag):
        global external_link_words, category_tag_words, token_count
        if(tag == "title"):
            self.title = 0
            title_text = self.title_data
            title_text = title_text + "\n"
            titleWrite(self.title_file_count, title_text)
            title_text = self.title_data.lower()
            title_text = re.split(pattern, title_text)

            token_count += len(title_text)

            for word in title_text:
                if word:
                    if word not in stop_words_dict and len(word)>2:
                        if word not in self.title_tag_words:
                            self.title_tag_words[word] = 1
                        else:
                            self.title_tag_words[word] += 1
            store_title_index(self.title_tag_words, self.page_count)
        if(tag=="text"):
            self.body_stat=0
            
            remove_redundant_body(self.body_content)

            try:
            # Getting Category Words
                cwords = self.body_content
                extractCategories(cwords, self.page_count)
            # Getting Info Box Words
                iwords = self.body_content
                processInfo(iwords, self.page_count)

            except:
                pass


            external_link_process(self.body_content, self.page_count)
            processContent(self.body_content, self.page_count)

            body_text = self.body_content
            body_text = body_regex.sub('==[A-Za-z]+==\n(.*)\n',body_text)
        
            body_text = body_text.lower()
            body_text = preprocess_word(body_text)
            body_text = re.split(pattern, body_text)

            token_count += len(body_text)

            for word in body_text:
                word = stemmer.stemWord(word)
                if word:
                    if word not in stop_words_dict and len(word)>2 and len(word) < 13:
                        if word not in self.body_words:
                            self.body_words[word] = 1
                        else:
                            self.body_words[word] += 1


            
            store_body_index(self.body_words, self.page_count)

            self.body_content = ""  
            external_link_words = dict() 
            category_tag_words = dict()
        



        
def dump_data_pickel():
    global word_position, index_path, token_count
    # print(word_position)
    # stat_path = sys.argv[3]
    # stat_file_write = open(stat_path, "a")
    # stat_file_write.write("Total Number of Tokens: " + str(token_count) + "\n")
    # stat_file_write.write("Total Number of Unique: " + str(len(word_position)) + "\n")
    # stat_file_write.close()
    # # print("Unique Count", len(word_position))
    file = open(index_path + "/wpos"+str(WikiHandler.title_file_count)+".pickle", "wb+")
    pickle.dump(word_position, file)
    file.close()         


def main():
    global title_index, body_index, dump_path, index_path, title_tags, token_count

    token_count = 0

    dump_path = sys.argv[1]
    index_path = sys.argv[2]
    if not os.path.exists(index_path):
        os.mkdir(index_path)

    title_tags = open(index_path + "/title0"+".txt", "w+")


    par=xml.sax.make_parser()
    Handler = WikiHandler()
    par.setFeature(xml.sax.handler.feature_namespaces,0)
    par.setContentHandler( Handler )
    par.parse(dump_path)
    # Writing Titles to File
    
    title_word_loc_write(WikiHandler.title_file_count)
    # Writing Title Position to Pickle File
    title_pos_pickle_write()
    # Writing Body Index to File

    body_word_loc_write(WikiHandler.title_file_count)

    # Writing Category Index to File
    category_word_loc_write(WikiHandler.title_file_count)

    # writing Info-Box index to file
    info_box_loc_write(WikiHandler.title_file_count)
    references_loc_write(WikiHandler.title_file_count)

    # Writing External Link Index in File
    ext_link_loc_write(WikiHandler.title_file_count)


    dump_data_pickel()

    # print("Token Count = ",token_count)
    
    

if __name__ == "__main__":                                          
    start = timeit.default_timer()
    build_stopWordsDict()
    main()
    stop = timeit.default_timer()
    print (stop - start)
