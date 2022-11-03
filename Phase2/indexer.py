from termios import tcdrain
import xml.sax
import sys
import os
import time
from collections import defaultdict, OrderedDict 
import re
from collections import defaultdict
from nltk.corpus import stopwords
from Stemmer import Stemmer


merge_path = "./temp/"
doc = 0
word_dict = defaultdict(dict)
title_list = ""
total_tokens = 0
dict_size = 15000
fcval = 0
title_doc_size = 15000
path = ""
word_set = set()
totfiles = 0



# =========================================== Pre-processing ===============================================================



stop_words = set()
stemmer = Stemmer('porter')


def pat_ret(type):
    if(type == 'info'):
        return re.compile(r'\{infobox')
    elif(type == 'cat'):
        return re.compile(r"\[\[category:(.*)\]\]")
    elif(type == 'ref'):
        return re.compile(r'==references==|== references ==|== references==|==references ==')
    elif(type == 'link'):
        return re.compile(r'==external links==|== external links ==|== external links==|==external links ==')
    

def build_stop_words():
    f = open("stopwords.txt", 'r')
    for line in f.readlines():
        stop_words.update(line)
    f.close()


def tok_txt(text):
    tcount = 0
    tokens = []
    text = re.split(r'[^A-Za-z0-9]+', text)
    
    
    for line in text:
        word = stemmer.stemWord(line)
        tc = 0
        if len(word) > 1:
            tc += 1
            if len(word) < 15: 
                if word not in stop_words:
                    tokens.append(word)
                else:
                    
                    continue
            else:
                tc = 0
                continue
        else:
            continue
    return tokens
    

def Info_ext(text):

    st_pattern = pat_ret('info')
    infobox_str = st_pattern.split(text)
    info_lis = []
    val_c = 0
    end_pattern = re.compile(r'\}\}\n(\w|\'|\n)')
    infobox_l = []
    dc = 0
    elec = 0
    if len(infobox_str):
        dc += 1
        for ele in infobox_str[1:]:
            data = end_pattern.split(ele)[0]
            elec += 1
            text = text.replace(data, '')
            info_lis.append(data)
        for ele in info_lis:
            for line in ele.split('\n'):
                elec += 1
                if len(line) and line[0] == '|':
                    value = line.split("=")
                    val_c += 1
                    if len(value) <= 1:
                        val_c = 0
                        continue
                    else:
                        value = tok_txt(value[1])
                        infobox_l += value     
                else:
                    continue
        elec = 0                
    return text, infobox_l


def cat_ext(text):
    cat_pat = pat_ret('cat')
    cat = cat_pat.findall(text)
    text = cat_pat.sub('', text)
    cat_char_c = len(text)
    cat_lis = []
    for line in cat:
        cat_lis += tok_txt(line)
    return text, cat_lis

def ref_regex(text):
    ref_pat = pat_ret('ref')
    ref = ref_pat.split(text)
    return ref



def ref_ext(text):
    ref =ref_regex(text)
    ref_c = 0
    refer = []
    if len(ref)>1:
        ref_c += 1
        ref = ref[1].split('\n')
        ref_c -= 1
        for sent in ref[2:]:
            if len(sent) and sent[0] !='*':
                ref_c = 0
                break
            if len(sent):
                ref_c += 1
                sent = re.sub(r'http\S+', '', sent)
                ref_c = 0
                refer += tok_txt(sent)
                text = text.replace(sent,'')
            else:
                continue
    else:
        return text, refer
      
    return text, refer


def link_ext(text):
    ext_pat = pat_ret('link')
    link = ext_pat.split(text)
    ext_c = 0
    links = []
    if len(link)>1:
        sent_len = 0
        link = link[1].split('\n')
        ext_c += 1
        for templ in link[2:]:
            ext_c = 1
            if len(templ) and templ[0] !='*':
                break
            elif len(templ):
                templ = re.sub(r'http\S+', '', templ)
                sent_len = len(templ)
                links += tok_txt(templ)
                sent_len += 1
                text = text.replace(templ,'')
                sent_len = 0
            else:
                continue
    else:
        return text, links
    return text, links


def ret_body_lis(text1):
    body = []
    for sent in text1.split('\n'):
        body += tok_txt(sent)
    return body

def bdy_ext(text1):
    text1 = re.sub(r'http\S+', '', text1) 
    text1 = text1[0:int(len(text1)*0.45)]
    return ret_body_lis(text1)





def preprocee_txt(title,text, doc):

    global word_set
    global total_tokens
    title = title.lower()
    title = tok_txt(title)
    c = 0
    text = text.lower()
    text, infobox = Info_ext(text)
    c += 1
    text, categories = cat_ext(text)
    c += 1
    text, references = ref_ext(text)
    c += 1
    text, links = link_ext(text)
    c += 1
    text1 = text
    body = bdy_ext(text1)

    return title, body, references, categories, links, infobox, c




# =========================================== Pre-processing Done ===============================================================





def write_title(title_list):
    global doc,title_doc_size
    global path
    if doc%title_doc_size==0:
        f = open(path+"/title/t"+str(doc//title_doc_size)+".txt", 'w')
        f.write(title_list)
        f.close()
    else:
        f = open(path+"/title/t"+str((doc//title_doc_size)+1)+".txt", 'w')
        f.write(title_list)
        f.close()


def title_dict_write(title):
    global word_dict
    global doc
    global fcval
    for i in title:
        if not (i in word_dict and doc in word_dict[i]):
            word_dict[i][doc] = [1,0,0,0,0,0]
        else:
            word_dict[i][doc][0] += 1

def body_dict_write(body):
    global word_dict
    global doc
    for i in body:
        if not (i in word_dict and doc in word_dict[i]):
            word_dict[i][doc] = [0,1,0,0,0,0]
        else:
            word_dict[i][doc][1] += 1


def references_dict_write(references):
    global word_dict
    global doc
    for i in references:
        if not (i in word_dict and doc in word_dict[i]):
            word_dict[i][doc] = [0,0,1,0,0,0]
        else:
            word_dict[i][doc][2] += 1


def categories_dict_write(categories):
    global word_dict
    global doc
    for i in categories:
        if not (i in word_dict and doc in word_dict[i]):
            word_dict[i][doc] = [0,0,0,1,0,0]
        else:
            word_dict[i][doc][3] += 1

def links_dict_write(links):
    global word_dict
    global doc
    for i in links:
        if not (i in word_dict and doc in word_dict[i]):
            word_dict[i][doc] = [0,0,0,0,1,0]
        else:
            word_dict[i][doc][4] += 1

def infobox_dict_write(infobox):
    global word_dict
    global doc
    for i in infobox:
        if not (i in word_dict and doc in word_dict[i]):
            word_dict[i][doc] = [0,0,0,0,0,1]
        else:
            word_dict[i][doc][5] += 1


def createIndex():

    global total_tokens
    global word_dict
    global doc
    
    word_dict = OrderedDict(sorted(word_dict.items()))
    k_c = 0
    if doc%dict_size ==0:
        fpath = path+"/temp/f"+(str(doc//dict_size))+".txt"
        f = open(fpath, 'w')
    else:
        fpath = path+"/temp/f"+(str((doc//dict_size)+1))+".txt"
        f = open(fpath, 'w')
    tag_idx = ['t','b','r','c','l','i']
    k_v = 0
    for k,v in word_dict.items():
        st = ""
        if len(v) > 15000:
            k_v = 0
            continue
        else:
            k_v += 1
            for k1, v1 in v.items():
                k_c += 1
                st += "d" + str(k1)
                for i in range(6):
                    if v1[i]:
                        k_c += 1
                        st += tag_idx[i] + str(v1[i])
                    else:
                        k_c = 0
                        continue
                st += '#'
            final_s = str(k)+" "+st+"\n"
            f.write(final_s)
    
    f.close()



def create_idx(title, body, references, categories, links, infobox):

    global word_dict
    global doc

    title_dict_write(title)
    
    body_dict_write(body)

    references_dict_write(references)
    
    categories_dict_write(categories)
    
    links_dict_write(links)

    infobox_dict_write(infobox)
    
    if doc%dict_size == 0:
        createIndex()
        word_dict = defaultdict(dict)



def update_tokens(titlelen, bodylen, referenceslen, categorieslen, linkslen, infoboxlen):
    global total_tokens
    total_tokens += titlelen + (bodylen) + (referenceslen) + (categorieslen) + (linkslen) + (infoboxlen)
    
def update_unique_words(title, body, references, categories, links, infobox):
    global word_set
    up_c = 0
    word_set.update(title)
    up_c += 1
    word_set.update(body)
    up_c += 1
    word_set.update(links)
    up_c += 1
    word_set.update(infobox)
    up_c += 1
    word_set.update(references)
    up_c += 1  
    word_set.update(categories)
    return up_c


class WikiHandler(xml.sax.ContentHandler):
    global word_dict
    global fcval
    def __init__(self):
        self.title = ''
        fcval = 0
        self.title_flg = ''
        self.other_flg = 0
        self.text = ''
        self.t_count = 0
        self.txt_flg = ''
        self.txt_count = 0
        
        self.other_content = ''
    def startElement(self, tag, attributes):
        if tag=="title":
            self.title_flg = 1 
            self.t_count += 1
            self.title = ""
        elif tag=="text":
            self.text = ""
            self.txt_flg = 1
        else:
            self.other_flg = 1
    def characters(self, content):
        if self.title_flg == 1:
            self.title += content
        elif self.txt_flg == 1:
            self.txt_count += 1
            self.text += content
        else:
            self.other_content += content
    def endElement(self, tag):
        global title_list
        global doc
        global total_tokens
        global word_set
        fcval = 0
        if tag=="title":
            self.title_flg = 0
            fcval += 1
            self.t_count = 0
            title_list += self.title + "\n"
        elif tag=="text":
            self.txt_flg = 0
            doc += 1
            self.txt_count = 0
            txt_val1 = ''
            fcval += 1
            txt_val1 += str(doc)
            title, body, references, categories, links, infobox, c1 = preprocee_txt(self.title, self.text, doc)
            txt_val1 = ''
            create_idx(title, body, references, categories, links, infobox)
            
            update_tokens(len(title), len(body), len(references), len(categories), len(links), len(infobox))
            update_unique_words(title, body, references, categories, links, infobox)
            if doc%title_doc_size == 0:
                print(str(doc) +" documents done. Time taken: "+str(time.time()-start))
                write_title(title_list)
                title_list = ""
            fcval = 0
        else:
            self.other_flg = 0
            self.other_content = ""

def parser_handler():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
    parser.parse(path_dump)
    write_title(title_list)
    createIndex()


# =========================================== INDEXING DONE ==========================================


# =========================================== MERGING START ==========================================


def open_files(file1, file2):
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    output_file = open("temp.txt", 'w')
    return f1, f2, output_file


def close_files(f1, f2, output_file):
    f1.close()
    f2.close()
    output_file.close()


def remove_file(file1, file2):
    os.remove(file1)
    os.remove(file2)


def individual(s1, s2, f1, f2, output_file):

    if s1:
        while s1:
            output_file.write(s1)
            s1 = f1.readline()
    
    if s2:
        while s2:
            output_file.write(s2)
            s2 = f2.readline()




def both_file(s1, s2, f1, f2, output_file):
    k_c1 = 0
    k_c2 = 0
    v_c1 = 0
    v_c2 = 0
    while s1 and s2:
        k1,v1 = s1.split(" ")
        if(k1):
            k_c1 +=1
        k2,v2 = s2.split(" ")
        if(k2):
            k_c2 +=1
        if k1 < k2:
            k_c1 = 0
            output_file.write(s1)
            v_c1 +=1
            s1 = f1.readline()

        elif k1 > k2:
            v_c2 +=1
            output_file.write(s2)
            k_c2 = 0
            s2 = f2.readline()
        else:
            k_c1 = 0
            v1 = v1.strip("\n")
            k_c2 = 0
            output_file.write(k1+" "+v1+v2)
            v_c1 = 0
            s1 = f1.readline()
            v_c2 = 0
            s2 = f2.readline()

    individual(s1, s2, f1, f2, output_file)
    


def mergeFiles(file1, file2, res, s):

    f1, f2, output_file = open_files(file1, file2)
    
    
    s1 = f1.readline()
    s2 = f2.readline()

    both_file(s1, s2, f1, f2, output_file)

    close_files(f1, f2, output_file)
    remove_file(file1, file2)
    os.rename("temp.txt", res)

    print("Files "+ file1 + " and " + file2 + " merged into "+ res)
    print()




def merge_main():
    dir_list = os.listdir(merge_path)
    merge_c = 0
    s = time.time()
    total_files = len(dir_list)
    merge_c += 1
    merge_f = 0
    while total_files !=1:
        if total_files % 2==0:
            merge_c -= 1
            for i in range(1,total_files,2):
                merge_fpath1 = merge_path+"f"+str(i)+".txt"
                merge_c += 1
                merge_fpath2 = merge_path+"f"+str(i+1)+".txt"
                merge_c += 1
                merge_fpath3 = merge_path+"f"+str((i+1)//2)+".txt"
                merge_c += 1
                mergeFiles(merge_fpath1, merge_fpath2, merge_fpath3, s)
        else:
            merge_c += 1
            for i in range(1,total_files-1,2):
                merge_fpath1 = merge_path+"f"+str(i)+".txt"
                merge_c += 1
                merge_fpath2 = merge_path+"f"+str(i+1)+".txt"
                merge_c += 1
                merge_fpath3 = merge_path+"f"+str((i+1)//2)+".txt"
                merge_c += 1
                mergeFiles(merge_fpath1, merge_fpath2, merge_fpath3, s)
            os.rename(merge_path+"f"+str(total_files)+".txt", merge_path+"f"+str((total_files+1)//2)+".txt")
        merge_f = 1
        dir_list = os.listdir(merge_path)
        total_files = len(dir_list)
        print("Files remaining : " , total_files)
    
    os.rename(merge_path+"f1.txt", merge_path+"d1.txt")


# =========================================== MERGING DONE ==========================================

# =========================================== SPLITTING START ========================================

def fopen(file1, file2):
    f1 = open(file1, 'r')
    f2 = open(file2, 'w')
    return f1, f2

def splitFile(file_to_split, s_idx_file, path, th ):

    f, secondary_index = fopen(file_to_split, s_idx_file)
    lines = []
    lc = 0
    fc_val = 1
    fc_test = 0
    line = f.readline()
        
    while line:
        lc += 1
        lines.append(line)
        if len(lines) == th:
            word = lines[0].split(" ")
            word_str = word[0]+"\n"
            secondary_index.write(word_str)
            temp_file_name = path+"f"+str(fc_val)+".txt"
            f_temp = open(temp_file_name, 'w')
            for i in lines:
                f_temp.write(i)
            f_temp.close()
            print("File Completed : ", fc_val)
            lines = []
            fc_test += 1
            fc_val += 1
        line = f.readline()

    fc_test = 0  
        
    
    if len(lines) > 0:
        word = lines[0].split(" ")
        word_str = word[0]+"\n"
        secondary_index.write(word_str)
        temp_file_name = path+"f"+str(fc_val)+".txt"
        f_temp = open(temp_file_name, 'w')
        for i in lines:
            f_temp.write(i)
        f_temp.close()
        lines = []
        fc_test += 1
        fc_val += 1 

    fc_test = 0   
    secondary_index.close()
    f.close()
    print("Total files are : ",fc_val)



def split_main():
    file_to_split = "./temp/d1.txt"
    s_idx_file = "./temp/secondary_index.txt"
    path = "./temp/"
    th = 15000
    splitFile(file_to_split, s_idx_file, path, th)




# =========================================== SPLITTING DONE ==========================================


def check_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)



if __name__ == "__main__" :
    build_stop_words()
    path_dump = sys.argv[1]
    path_inverted_index = sys.argv[2]
    check_folder(path_inverted_index)
    path = path_inverted_index
    check_folder(path_inverted_index+"/temp")
    check_folder(path_inverted_index+"/title")
        
    start = time.time()

    parser_handler()

    stop = time.time()
    print("Time in indexing : ", stop-start)


    # Merging Files
    merge_main()

    # Spiltting the Merged Files
    split_main()





    
