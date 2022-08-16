import pickle

objects = []
with (open("temp/wpos0.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break


# obj = pd.read_pickle(r'temp/wpos0.pickle')

print(objects[:1000])