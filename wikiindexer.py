import timeit
import xml.sax
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from collections import defaultdict
import pickle
import re 


stemmer = nltk.stem.SnowballStemmer('english')
stop_words_dict= defaultdict(int)
pattern = re.compile("[^a-zA-Z0-9]")
# RE to remove urls
regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
# RE to remove tags & css
regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
title_pos = list() # Which title is present at which location in the file
title_index = defaultdict(list)
# body_index = defaultdict(list)
category_index = defaultdict(list)
info_box_index = defaultdict(list)
ext_links_index = defaultdict(list)
word_position = dict()
title_tags = open("temp/title0"+".txt", "w+")


def preprocess(word):
    global stemmer
    word = word.strip()
    word = word.lower()
    
    word = stemmer.stem(word)
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
    
    
# def body_word_loc_write(file_count):
#     global body_index, word_position
    
#     fptr=0
#     file = "temp/bword_idx"+str(file_count)+".txt"
#     outfile = open(file, "w+")
#     for word in body_index:
#         index = ",".join(body_index[word])+"\n"
#         outfile.write(index)
#         if word in word_position :
#             word_position[word]['b']=fptr
#         else:
#             word_position[word] = {}
#             word_position[word]['b']=fptr
#         fptr = fptr + len(index)
#     outfile.close()


def category_word_loc_write(file_count):
    global category_index, word_position
    fptr=0
    file = "temp/cword_idx"+str(file_count)+".txt"
    outfile = open(file, "w+")
    for word in category_index:
        index = ",".join(category_index[word])+"\n"
        # print(index)
        if word in word_position :
            word_position[word]['c']=fptr
        else:
            word_position[word] = {}
            word_position[word]['c']=fptr
        outfile.write(str(index))
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
        # print("word", word)
        if word in word_position :
            word_position[word]['i']=fptr
        else:
            word_position[word] = {}
            word_position[word]['i']=fptr
        outfile.write(index)
        fptr = fptr + len(index)
    outfile.close()

def ext_link_loc_write(file_count):
    global ext_links_index, word_position
    fptr = 0
    file = "temp/ext_link_idx"+str(file_count)+".txt"
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

# def store_body_index(body_tag_words, page_count):
#     global body_index
#     index = str(page_count)
#     for word in body_tag_words :
#         s = index + ":" + str(body_tag_words[word])
#         body_index[word].append(s)



def store_category_index(category_tag_words, page_count):
    global category_index
    index = str(page_count)
    for word in category_tag_words :
        s = index + ":" + str(category_tag_words[word])
        category_index[word].append(s)

def store_info_box_index(info_box_words, page_count):
    # print(info_box_words)
    global info_box_index
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
    global stemmer
    text = (ext_link_cont.split("==External links=="))
    if len(text)>1:
        text=text[1].split("\n")[1:]
        for txt in text:
            if txt=='':
                break
            if txt[0]=='*':
                txt = stemmer.stem(txt)
                text_split=txt.split(' ')
                link=[wd for wd in text_split if 'http' not in wd]
                link=' '.join(link)
                links+=' '+link
    external_link_words = dict()
    links = links.replace('\n', ' ').replace('File:', ' ')
    links = re.sub('(http://[^ ]+)', ' ', links)
    links = re.sub('(https://[^ ]+)', ' ', links)
    links = re.sub('\{.*?\}|\[.*?\]|\=\=.*?\=\=', ' ', links)
    links = ''.join([i if ord(i) < 128 else ' ' for i in links])
    links = ''.join(ch if ch.isalnum() else ' ' for ch in links)
    links = links.split()
    for word in links:
        if word:
            word = word.lower()
            if word not in stop_words_dict and len(word)>2:
                if word not in external_link_words:
                    external_link_words[word] = 1
                else:
                    external_link_words[word] += 1
    store_ext_links_index(external_link_words, page_count)


def tokenizeInfo(text):
    global stemmer
    text = re.split(r'[^A-Za-z0-9]+', text)
    tokens = []
    for line in text:
        word = stemmer.stem(line)
        if len(word) > 2 and len(word) < 20 and word not in stop_words_dict:
            tokens.append(word)
    return tokens


def extractCategories(text, page_count):
    cat = re.findall(r"\[\[category:(.*)\]\]", text)
    d = {}
    for line in cat:
        words = tokenizeInfo(line)
        for i in words:
            if i in d:
                d[i] = d[i]+1
            else:
                d[i] = 1
    # print(d)
    store_category_index(d, page_count)


def processInfo(text, page_count):
    # print(text)
    cont = text.split("{{infobox")
    info = []
    if len(cont) <= 1:
        return
    flag= False
    for infob in cont:
        traw = infob.split("\n")
        if (not flag):
            flag=True
        else :
            for lines in traw:
                if lines == "}}":
                    break
                info += tokenizeInfo(lines)
    info_box_words = {}
    for i in info:
        if i in info_box_words:
            info_box_words[i] = info_box_words[i]+1
        else:
            info_box_words[i] = 1
    
    store_info_box_index(info_box_words, page_count)
    # print(d)

def refandextType(name):
	l = []
	l.append("==" + name + "==")
	l.append("== " + name + "==")		
	l.append("==" + name + " ==")		
	l.append("== " + name + " ==")		
	return l

def processContent(text, page_count):
    text=text.lower()
    references={}
    links={}
    # categories={}
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

        extractCategories(data[0], page_count)

        haslink=1
        catdata=data[0].split(ext[0])
        if len(catdata)==1:
            catdata=data[0].split(ext[1])
        if len(catdata)==1:
            catdata=data[0].split(ext[2])
        if len(catdata)==1:
            catdata=data[0].split(ext[3])
        if len(catdata)==1:
            links={}
            haslink=0
        # if (haslink):
        #     links=extractLinks(catdata[1])
    else:
        haslink=1
        catdata=data[1].split(ext[0])
        if len(catdata)==1:
            catdata=data[1].split(ext[1])
        if len(catdata)==1:
            catdata=data[1].split(ext[2])
        if len(catdata)==1:
            catdata=data[1].split(ext[3])
        if len(catdata)==1:
            links={}
            haslink=0
        # if (haslink):
        #     links = extractLinks(catdata[1])
        
        # references = getReferences(data[1])
        extractCategories(data[1], page_count)
 
    # infobox= getInfobox(data[0])
    # body = tokenize(data[0])
    # d = {}
    # for i in body:
    # 	if i in d:
    # 		d[i] = d[i]+1
    # 	else:
    # 		d[i] = 1
    # return d, references, categories, links, infobox

    


    processInfo(data[0], page_count)
    # extractCategories(data[1], page_count)


class WikiHandler(xml.sax.ContentHandler):
    title_file_count = 0
    ext_link_cont = ""
    def __init__(self):
        self.title=0
        self.title_data = ""
        self.page_count = 0 # For Counting the pages Parsed till now
        self.title_count = 0 # Counting title for 1 title file
        self.title_file_count = 0
        self.title_id_stat = 0
        self.page_stat = 0
        self.title_tag_words = dict() # For Storing the Title Tag Words
        self.category_words = dict() # For Storing the Category Words
        self.body_stat = 0
        self.ext_link_cont = ""

    
    def startElement(self,tag,attr):
        if(tag=="id" and self.page_stat==0):
            self.page_stat=1
            self.title_id_stat=1
        if(tag == "title"):
            self.title = 1
            self.title_data = ""
        if(tag == "page"):
            self.page_count = self.page_count + 1
            self.title_count = self.title_count + 1
            self.title_tag_words = dict() # Making the Title tag dictionary as empty for every page
        if(tag == "text"):
            self.body_stat = 1
        

    def characters(self, content):
        global pattern, regExp1, regExp2, title_pos
        if(self.title == 1):
            self.title_data += content
            # Adding title content to the dictionary
            
        if(self.body_stat == 1):
            self.ext_link_cont += content
            global stemmer
            body_text = content
            body_text = regExp1.sub('',body_text)
            body_text = regExp2.sub('',body_text)
    
            # cat = re.findall(r"\[\[category:(.*)\]\]", body_text)
            # for line in cat:
            #     words = tokenizeInfo(line)
            #     for i in words:
            #         if i in self.category_words:
            #             self.category_words[i] = self.category_words[i]+1
            #         else:
            #             self.category_words[i] = 1
          
            # try :
            #     temp_category_word = re.findall("\[\[Category:(.*?)\]\]", body_text)
            #     if temp_category_word:
            #         for w in temp_category_word:
            #             w = re.split(pattern, w)
            #             for word in w:
            #                 word = preprocess(word)
            #                 # print(word)
            #                 if word:
            #                     if len(word) <= 2 :
            #                             continue
            #                     if word not in stop_words_dict :
            #                         if word not in self.category_words:
            #                             self.category_words[word] = 1
            #                         else:
            #                             self.category_words[word] += 1
            # except :
            #     pass
            # print(body_text)  
            # processInfo(body_text)

            


            # body_text = body_text.lower()
            # body_text = re.split(pattern, body_text)
            # for word in body_text:
            #     if word:
                    
            #         word = stemmer.stem(word)
            #         if word not in stop_words_dict and len(word)>2:
            #             if word not in self.body_words:
            #                 self.body_words[word] = 1
            #             else:
            #                 self.body_words[word] += 1
           
    def endElement(self, tag):
        if(tag=="page"):
            self.page_stat=0
            self.title_count+=1         
        if(tag=="id"):
            self.title_id_stat=0
        if(tag == "title"):
            self.title = 0
            title_text = self.title_data
            title_text = title_text + "\n"
            titleWrite(self.title_file_count, title_text)
            title_text = self.title_data.lower()
            title_text = re.split(pattern, title_text)
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
            # store_body_index(self.body_words, self.page_count)
            # store_category_index(self.category_words, self.page_count)
            # store_info_box_index(self.info_box_words, self.page_count)
            external_link_process(self.ext_link_cont, self.page_count)
            processContent(self.ext_link_cont, self.page_count)
            self.ext_link_cont = ""   
            # WikiHandler.Index_Create_Fun(self)



        
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
    par.parse('data.xml')
    # Parsing Done
    # Writing Titles to File
    
    title_word_loc_write(WikiHandler.title_file_count)
    # Writing Title Position to Pickle File
    title_pos_pickle_write()
    # Writing Body Index to File

    # body_word_loc_write(WikiHandler.title_file_count)

    # Writing Category Index to File
    category_word_loc_write(WikiHandler.title_file_count)

    # writing Info-Box index to file
    info_box_loc_write(WikiHandler.title_file_count)

    # Writing External Link Index in File
    ext_link_loc_write(WikiHandler.title_file_count)


    dump_data_pickel()
    
    

if __name__ == "__main__":                                          
    start = timeit.default_timer()
    build_stopWordsDict()
    main()
    stop = timeit.default_timer()
    print (stop - start)
