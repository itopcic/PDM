import json
import pandas as pd
import sys

# Remove columns for each of the features which have only 2 instances
# This script is used in the do_svm.sh bash script which automatically computes the SVM for a pair of Subreddits

if len(sys.argv) == 3:
    features = pd.read_csv(sys.argv[1])
    with open(sys.argv[2], "r") as file:
        feats_list = json.load(file)
    new_feats_list = []
    for feat in feats_list:
        if feat[1] < 2:
            features.drop(feat[0], axis=1)
        else:
            new_feats_list.append(feat)
    features.to_csv(sys.argv[1], index=False)
    with open(sys.argv[2], "w") as file:
        json.dump(new_feats_list, file)
else:
    print("Not the correct number of arguments")