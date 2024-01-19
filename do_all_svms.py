import os

from utils import pairs

# Simple script to compute the SVM for all the pairs of Subreddits

for pair in pairs:
    print("Pair : " + " ".join(pair))
    os.system(f"./do_svm.sh {pair[0]} {pair[1]}")
