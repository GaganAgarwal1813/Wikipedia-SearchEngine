from dataclasses import field
import sys
import pickle
import nltk

stemmer = nltk.stem.SnowballStemmer('english')
def preprocess(word):
    word = word.strip()
    word = word.lower()
    stemmer = nltk.stem.SnowballStemmer('english')
    word = stemmer.stem(word)
    return word

def title_test(query):
    field = 't'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    # print(title_tags)
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    title_idx = open("temp/tword_idx0.txt", "r")
    if query in word_position and field in word_position[query]:
        position = word_position[query]['t']
        title_idx.seek(position)
        s = title_idx.readline()
        # print(s)
        s = s.split(',')
        for ele in s:
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
        # print(s)


def body_test(query):
    query =preprocess(query)
    field = 'b'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    body_idx = open("temp/bword_idx0.txt", "r")
    if query in word_position and field in word_position[query]:
        position = word_position[query]['b']
        body_idx.seek(position)
        s = body_idx.readline()
        s = s.split(',')
        for ele in s:
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
       

def category_search(query):
    query =preprocess(query)
    field = 'c'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/cword_idx0.txt", "r")
   
    if query in word_position and field in word_position[query]:
        position = word_position[query]['c']
       
        body_idx.seek(position)
        s = body_idx.readline()
        
        s = s.split(',')
        for ele in s:
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
        # print(s)

def info_search(query):
    query =preprocess(query)
    field = 'i'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/info_box_idx0.txt", "r")
   
    if query in word_position and field in word_position[query]:
        position = word_position[query]['i']
       
        body_idx.seek(position)
        s = body_idx.readline()
        
        s = s.split(',')
        for ele in s:
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                # print(title_file.readline())
        # print(s)


def ext_search(query):
    # print(query)
    field = 'e'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/ext_link_idx0.txt", "r")
   
    if query in word_position and field in word_position[query]:
        position = word_position[query]['e']
       
        body_idx.seek(position)
        s = body_idx.readline()
        
        s = s.split(',')
        for ele in s:
            # print(ele)
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
        # print(s)


def info(query):
    # print(query)
    global stemmer
    query = stemmer.stem(query)
    field = 'i'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/info_box_idx0.txt", "r")
   
    if query in word_position and field in word_position[query]:
        position = word_position[query]['i']
       
        body_idx.seek(position)
        s = body_idx.readline()
        
        s = s.split(',')
        for ele in s:
            # print(ele)
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
        # print(s)

def references(query):
    # print(query)
    global stemmer
    query = stemmer.stem(query)
    field = 'r'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/references_idx0.txt", "r")
   
    if query in word_position and field in word_position[query]:
        position = word_position[query]['r']
       
        body_idx.seek(position)
        s = body_idx.readline()
        
        s = s.split(',')
        for ele in s:
            # print(ele)
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
        # print(s)

def body(query):
    # print(query)
    # global stemmer
    # query = stemmer.stem(query)
    field = 'b'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/bword_idx0.txt", "r")
   
    if query in word_position and field in word_position[query]:
        position = word_position[query]['b']
       
        body_idx.seek(position)
        s = body_idx.readline()
        
        s = s.split(',')
        for ele in s:
            # print(ele)
            if ele:
                ele = ele.split(':')
                title_file.seek(title_tags[int(ele[0])-1])
                print(title_file.readline())
        # print(s)

def main():
    query = sys.argv[1]
    query = query.lower()
    # title_test(query)
    # category_search(query)
    # ext_search(query)
    # info(query)
    # references(query)
    body(query)

if __name__ == "__main__":
    main()