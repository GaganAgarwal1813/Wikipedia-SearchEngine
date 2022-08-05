import sys
import pickle
import nltk

stemmer = nltk.stem.SnowballStemmer('english')

def main():
    query = sys.argv[1]
    title_file = open("temp/title0.txt", "r")
    title_tags = pickle.load(open("temp/title_pos.pickle", "rb"))
    # print(title_tags)
    word_position = pickle.load(open("temp/wpos0.pickle", "rb"))
    title_idx = open("temp/tword_idx0.txt", "r")
    if query in word_position:
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


if __name__ == "__main__":
    main()