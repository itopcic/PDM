import json

from utils import pairs, texts_len

#Simple script to verify that the SVM texts are correctly tokenized and that there are the correct number of text per user
for pair in pairs:
    folder = "_".join(pair)
    for sub in pair:
        with open("pairs/" + folder + "/" + sub + ".json") as f:
            d = json.load(f)
            print("There are " + str(len(d.keys())) + " users")
            for user in d.keys():
                good = all(map(lambda t: len(t) == texts_len, d[user]))
                if not good or len(d[user]) != 10:
                    print(user + " is bad")
                    print(len(d[user]))
                    for s in d[user]:
                        if len(s) != texts_len:
                            print(s)
