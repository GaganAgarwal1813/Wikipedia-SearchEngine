import time
from collections import defaultdict
import re
from Stemmer import Stemmer
import sys


stop_words = defaultdict()
stemmer = Stemmer('porter')



def build_stopword_dict():
    global stop_words
    stc = 0
    with open ('stopwords.txt','r') as f:
        for i in f:
            i=i.strip(' ').strip("\n")
            stc = stc+1
            stop_words[i]=1
    return stc


def query_process(query):
    query = re.split(r'[^A-Za-z0-9]+', query)
    token_c = 0
    tokens = []
    for line in query:
        word = stemmer.stemWord(line)
        if len(word) > 1:
            if len(word) < 15 :
                if word in stop_words:
                    continue
                else:
                    tokens.append(word)
            else:
                continue
        else:
            continue
    token_c = len(tokens)
    # print("Number of tokens: ", token_c)
    return tokens


def extract(s):

    
    acount = 0
    d = 0
    qc = 0
    ocount = 1
    c = -1
    result_dict = {}
    for i in range(0,len(s)):
        qc += 1
        if ord(s[i])>=97 and ord(s[i])<=122:
            if c!=-1:
                acount += 1
                result_dict[c] = d 
                d = 0   
            ocount = 0
            c = s[i]
        else:
            acount = 0
            d = d*10 + ord(s[i])-48
            ocount += 1
    result_dict[c] = d

    return result_dict




def get_id(i):

    proper_parts = 0
    improper_part = 0

    if i%15000:
        proper_parts += 1
        fn = (i//15000)+1
    else:
        improper_part += 1
        fn = i//15000 + 1
    return fn



def get_doc_num(f,i):
    c = 0
    for j in f.readlines():
        c = c+1
        if c==i%15000:
            return j
        else:
            continue
        
    return -1


def get_doc_name(i):
    fn = get_id(i)
    f = open(path+"/title/t"+str(fn)+".txt", 'r')
    return get_doc_num(f,i)


def calcScore(data):
    score = 0
    
    weights = weight_initialise()
    data_num = 0
    tags = ['t','b','c','r','l','i']
    for i in tags:
        if i in data:
            data_num += 1
            score += data[i] * weights[i]
    if 'd' in data:
        data_num = 0
        return data['d'], score

    return -1,-1


def calcScoreField(data, k):
    score = 0
    weights = weight_initialise()
    if k in data:
        c = data[k]
        w = weights[k]
        score += c * w
    if 'd' in data:
        return data['d'], score

    return -1,-1

def weight_initialise():
    data_weight = {}
    r_weigh = 10
    data_weight['r']= r_weigh
    
    l_weigh = 10
    data_weight['l']= l_weigh
    i_weigh = 5
    data_weight['i']= 5 * i_weigh
    t_weigh = 10
    data_weight['t']= 5 * t_weigh
    c_weigh = 10
    data_weight['c']= c_weigh

    data_weight['b']= 5
    
    
    
    
    return data_weight






def det_find(d,k='a',field=False):
    scores = {}
    s = set()
    sc = 0
    
    dcount = 0
    d = d.split("#")
    fcount = 0
    for word in d:
        data = extract(word)
        if field:
            fcount += 1
            doc_num, score = calcScoreField(data, k)
            sc = 0
        else:
            sc += 1
            doc_num, score = calcScore(data)
            dcount = 0
        if doc_num !=1:
            fcount = 0
            scores[doc_num] = score
            dcount += 1
            s.add(doc_num)
    
    return s, scores


def file_number_fun(word, sc_q_lis):

    i = 0
    itercount = 0
    j = len(sc_q_lis)-1
    left_skewed = 0
    right_skewed = 0
    while i<j:
        itercount += 1
        mid = (i+j)//2
        if sc_q_lis[mid] <= word:
            right_skewed += 1
            i = mid+1
        elif sc_q_lis[mid] > word:
            left_skewed += 1
            j = mid

    return i



def calculate_score_dict(query, final_set, l):
    qc = 0
    unique_w = 0
    score_dict = {}
    total_wc = 0
    word_in_dic = 0
    for i in range(len(query)):
        qc += 1
        for j in final_set:
            total_wc += 1
            if j!=-1:
                if j in score_dict:
                    total_wc -= 1
                    score_dict[j] += l[query[i]][j]
                else:
                    unique_w += 1
                    score_dict[j] = l[query[i]][j]
                    word_in_dic += 1
            else:
                continue
    a = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    return a


def n_query(query):
    qc = 0
    query = query_process(query)
    wc = 0
    appc = 0
    l = {}
    sets = []
    count_ele = 0
    final_set = []
    fcount = 0
    for i in range(len(query)):
        qc += 1
        fno = file_number_fun(query[i], sc_q_lis)
        f  = open(path+"/temp/f"+str(fno)+".txt", 'r')
        fcount += 1
        for line in f.readlines():
            a, b = line.split(" ")
            wc += 1
            if a==query[i]:
                appc = appc + 1
                s, ans = det_find(b)
                sets.append(s)
                count_ele += 1
                l[a] = ans 
                break
        f.close()

    set_val = len(sets)
    cset_val = 0
    if set_val>0:
        final_set = sets[0]
        fcount = 0
    for i in range(1, len(sets)):
        cset_val += 1
        final_set = final_set.intersection(sets[i])
    
    return calculate_score_dict(query, final_set, l)


def f_query(query):

    dic_query = {}
    unique_qc = 0
    query = query.split(":")
    
    c = query[0]
    qc = len(query)
    for i in range(1,len(query)):
        qc += 1
        if i!= len(query)-1:
            dic_query[c] = (query[i])[0:len(query[i])-2]
            unique_qc += 1
            c = (query[i])[len(query[i])-1]
        else:
            unique_qc -= 1
            dic_query[c] = query[i]
    
    l = {}
    sets = []    
    pre_process_stat = 0
    fc = 0
    final_set = []
    for k,v in dic_query.items():    
        v = query_process(v)
        pre_process_stat = 1
        for i in range(len(v)):
            fno = file_number_fun(v[i], sc_q_lis)
            fc = fc + 1
            f  = open(path+"/temp/f"+str(fno)+".txt", 'r')
            lc = 0
            for line in f.readlines():
                a, b = line.split(" ")
                lc += 1
                if a==v[i]:
                    s, ans = det_find(b,k,True)
                    pre_process_stat = 0
                    sets.append(s)
                    l[a] = ans 
                    break
            lc = 0
            f.close()
            fc = 0
    set_ele = 0
    if len(sets)>0:
        set_ele += 1
        final_set = sets[0]
    for i in range(1, len(sets)):
        set_ele += 1
        final_set = final_set.intersection(sets[i])

    return calculate_score_dict(v, final_set, l)


def ans_write(ans, ans_fp):
    c = 0
    line_c = 0
    for i in ans:
        data_to_write = str(i[0])+", "+get_doc_name(i[0])
        ans_fp.write(data_to_write)
        line_c += 1
        c+=1
        if c!=10:
            continue
        else:
            break


def query_identify(query):
    nqcount = 0
    query = query.lower()
    if 't:' in query:
        ans = f_query(query)
    elif 'i:' in query:
        ans = f_query(query)
    elif 'b:' in query:
        ans = f_query(query)
    elif 'c:' in query:
        ans = f_query(query)
    elif 'r:' in query:
        ans = f_query(query)
    elif 'l:' in query:
        ans = f_query(query)
    else:
        nqcount += 1
        ans = n_query(query)
    return ans


def build_sec_lis(path):
    sec_idx = open(path+"/temp/secondary_index.txt",'r')
    wc = 0
    sc_q_lis = []
    for i in sec_idx.readlines():
        wc += 1
        sc_q_lis.append(i.strip("\n"))
    sec_idx.close()
    wc = 0
    return sc_q_lis

    

if __name__ == '__main__':
    build_stopword_dict()
    sc_q_lis = []
    path = "." 
    qpath = sys.argv[1]
    queries = open(qpath,'r')
    sc_q_lis = build_sec_lis(path)
   
    
    ans_fp = open('./ans.txt','w')
    

    for query in queries.readlines():
        start = time.time()
        ans = query_identify(query)
        ans_write(ans, ans_fp)
        end = time.time()
        ans_fp.write(str(end-start)+"\n\n")
        
    queries.close()
    ans_fp.close()