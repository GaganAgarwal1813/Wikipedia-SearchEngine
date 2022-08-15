from dataclasses import field
import sys
import pickle
# import nltk
from Stemmer import Stemmer

stemmer = Stemmer('porter')
def preprocess(word):
    word = word.strip()
    word = word.lower()
    word = stemmer.stemWord(word)
    return word

def title_test(query1):
    ans = []
    # query1 = preprocess(query1)
    field = 't'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    title_idx = open("temp/tword_idx0.txt", "r")
    query1 = query1.split(' ')
    for query in query1:
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
                    # print(title_file.readline())
                    ans.append(title_file.readline())
            # print(s)
    return ans


# def body_test(query):
#     query =preprocess(query)
#     field = 'b'
#     title_file = open("temp/title0.txt", "r")
#     title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
#     word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
#     body_idx = open("temp/bword_idx0.txt", "r")
#     if query in word_position and field in word_position[query]:
#         position = word_position[query]['b']
#         body_idx.seek(position)
#         s = body_idx.readline()
#         s = s.split(',')
#         for ele in s:
#             if ele:
#                 ele = ele.split(':')
#                 title_file.seek(title_tags[int(ele[0])-1])
#                 print(title_file.readline())
       

def category_search(query1):
    ans = []
    query1 =preprocess(query1)
    field = 'c'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/cword_idx0.txt", "r")
    
    query1 = query1.split(' ')
    for query in query1:
        if query in word_position and field in word_position[query]:
            position = word_position[query]['c']
        
            body_idx.seek(position)
            s = body_idx.readline()
            
            s = s.split(',')
            for ele in s:
                if ele:
                    ele = ele.split(':')
                    title_file.seek(title_tags[int(ele[0])-1])
                    # print(title_file.readline())
                    ans.append(title_file.readline())
            # print(s)
    return ans

# def info_search(query1):
#     query1 =preprocess(query1)
#     field = 'i'
#     title_file = open("temp/title0.txt", "r")
#     title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
#     word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
#     body_idx = open("temp/info_box_idx0.txt", "r")
#     query1 = query1.split(' ')
#     for query in query1:
#         if query in word_position and field in word_position[query]:
#             position = word_position[query]['i']
        
#             body_idx.seek(position)
#             s = body_idx.readline()
            
#             s = s.split(',')
#             for ele in s:
#                 if ele:
#                     ele = ele.split(':')
#                     title_file.seek(title_tags[int(ele[0])-1])
#                     # print(title_file.readline())
#             # print(s)


def ext_search(query1):
    ans = []
    query1 = preprocess(query1)
    field = 'e'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/ext_link_idx0.txt", "r")
   
    query1 = query1.split(' ')
    for query in query1:
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
                    # print(title_file.readline())
                    ans.append(title_file.readline())
            # print(s)
    return ans

def info(query1):
    ans = []
    query1 = preprocess(query1)
    field = 'i'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/info_box_idx0.txt", "r")
   
    query1 = query1.split(' ')
    for query in query1:
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
                    # print(title_file.readline())
                    ans.append(title_file.readline())
            # print(s)
    return ans

def references(query1):
    ans = []
    query1 = preprocess(query1)
    field = 'r'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/references_idx0.txt", "r")
    query1 = query1.split(' ')
    for query in query1:
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
                    # print(title_file.readline())
                    ans.append(title_file.readline())
            # print(s)
    return ans

def body(query1):
    # print(query)
    ans = []
    query1 = preprocess(query1)
    field = 'b'
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    
    body_idx = open("temp/bword_idx0.txt", "r")
    
    # print(query1)
    query1 = query1.split(' ')
    for query in query1:
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
                    # print(title_file.readline())
                    ans.append(title_file.readline())
            # print(s)
    return ans

def main():
    query = sys.argv[1]
    query = query.lower()
    print(title_test(query))
    # print(category_search(query))
    # print(ext_search(query))
    # print(info(query))
    # print(references(query))
    # print(body(query))

if __name__ == "__main__":
    main()