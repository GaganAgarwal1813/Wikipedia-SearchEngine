# import string
# from nltk import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer
# from nltk import pos_tag



# def stem(datalist):                                        #Stemming the data
#     finalLis=[]
#     stemmer = nltk.stem.SnowballStemmer('english')
#     for i in datalist:
#         finalLis.append(stemmer.stem(i))
#     return finalLis

# def makeDict(datalist):
#     datalist = removeStopWords(datalist)
#     p=[]
#     temp=defaultdict(int)
#     datalist= stem(datalist)

#     for x in datalist:
#         temp[x]=temp[x]+1
#     return temp

# def preProcess(text):
#     # Converting to lower case
#     text = text.lower()
#     # Removing all the special characters
#     text_p = "".join([char for char in text if char not in string.punctuation])
#     # Tokenizing the text
#     tokens = word_tokenize(text_p)
#     # Removing stop words
#     tokens = removeStopWords(tokens)
#     # Stemming the tokens
#     ps = PorterStemmer()
#     tokens = [ps.stem(word) for word in tokens]
#     return tokens

# def processTitle(data):
#     data=data.lower()
#     data_tok=re.findall(r'\d+|[\w]+',data)
#     temp=makeDict(data_tok)
#     return temp  

# def removeStopWords(dataLis):                           # Removing Stop Words
#     temp=[key for key in dataLis if stop_words_dict[key]!=1]
#     return temp