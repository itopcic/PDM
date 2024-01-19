import json
import numpy as np
import os

from utils import texts_len, test_len, min_len

# This file contains the function used by the SVM txt files creator to create split files which tell SuperStyl which
# text to use for training data and which to use for testing.

max_users = 6

# Generates the split file for a single Subreddit
def generate_split(pair, output_folder):
    folder = "_".join(pair)

    users = []
    # Load the texts
    with open("/home/topcic/Documents/PDM/pairs/" + folder + "/" + pair[0] + ".json", "r") as file:
        users = json.load(file).keys()

    # Generate the training and testing filenames
    train = []
    valid = []
    train_len = int(min_len / texts_len) - test_len
    for user in list(users)[:max_users]:
        valid += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, test_len)), map(str, range(test_len)))))
        train += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, train_len)), map(str, range(test_len, test_len + train_len)))))

    if not output_folder.endswith("/"):
        output_folder += "/"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Write the split.json file
    with open(output_folder + "split.json", "w") as file:
        json.dump({"train": train, "valid": valid, "elim": []}, file)
        
# Generates the split file for two Subreddits
def generate_split_double(pair, output_folder, length):
    folder = "_".join(pair)

    users = []
    
    # Load the texts
    with open("/home/topcic/Documents/PDM/pairs/" + folder + "/" + pair[0] + ".json", "r") as file:
        users = json.load(file).keys()

    # Generate the training and testing filenames
    train = []
    valid = []
    for user in list(users)[:max_users]:
        valid += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, length)), map(str, range(length)))))
        train += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, length)), map(str, range(length, 2*length)))))

    if not output_folder.endswith("/"):
        output_folder += "/"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    # Write the split.json file    
    with open(output_folder + "split.json", "w") as file:
        json.dump({"train": train, "valid": valid, "elim": []}, file)

# Generate the split.json file for the topic confustion task
def generate_split_confusion(pair, output_folder, length):
    folder = "_".join(pair)

    with open("/home/topcic/Documents/PDM/pairs/" + folder + "/" + pair[0] + ".json", "r") as file:
        users_one = json.load(file).keys()
        
    with open("/home/topcic/Documents/PDM/pairs/" + folder + "/" + pair[1] + ".json", "r") as file:
        users_two = json.load(file).keys()
        
    if len(users_one) >= len(users_two):
        users = list(users_two)[:max_users]
    else:
        users = list(users_one)[:max_users]

    half = int(len(users)/2)
    
    train = []
    valid = []
    for user in users[:half]:
        valid += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, length)), map(str, range(length)))))
        train += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, length)), map(str, range(length, 2*length)))))
        
    for user in users[half:]:
        valid += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, length)), map(str, range(length, 2*length)))))
        train += list(map(lambda p: "_".join(p), zip(list(np.repeat(user, length)), map(str, range(length)))))

    if not output_folder.endswith("/"):
        output_folder += "/"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        
    with open(output_folder + "split.json", "w") as file:
        json.dump({"train": train, "valid": valid, "elim": []}, file)
