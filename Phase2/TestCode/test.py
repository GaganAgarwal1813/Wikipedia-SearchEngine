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


def preProcess(fname):
    file_pointer = open(fname, "r")
    text = file_pointer.read()
    # Converting to lower case
    text = text.lower()
    # Removing all the special characters
    text_p = "".join([char for char in text if char not in string.punctuation])
    # Tokenizing the text
    tokens = word_tokenize(text_p)
    # Removing stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    # Stemming the tokens
    ps = PorterStemmer()
    tokens = [ps.stem(word) for word in tokens]
    return tokens



def test():
    fp=open("test","w")
    data = "\n".join(preProcess("temp/title0"))
    # print(data)
    fp.write(data)

def main():
    test()

if __name__ == "__main__":
    main()