import json
import os

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from utils import pairs
from generate_split import *

# Create files for use as input for SuperStyl. The data has to be arranged as txt files in a folder for each Subreddit
# We also create txt files for with POS tagged texts and Lemmatized texts

texts_folder = "texts/"

normal_folder = "normal/"
texts_pos_folder = "POS/"
texts_lemma_folder = "Lemma/"

# Generates the input data for one Subreddit
def generate_txt_single(sub, folder):
    # Load the texts
    with open("pairs/" + folder + "/" + sub + ".json", "r") as file:
        texts = json.load(file)
        
    # Create folders that do not exist
    if not os.path.exists(texts_folder + sub):
        os.mkdir(texts_folder + sub)

    if not os.path.exists(texts_folder + sub + "/" + normal_folder):
        os.mkdir(texts_folder + sub + "/" + normal_folder)

    if not os.path.exists(texts_folder + sub + "/" + texts_pos_folder):
        os.mkdir(texts_folder + sub + "/" + texts_pos_folder)

    if not os.path.exists(texts_folder + sub + "/" + texts_lemma_folder):
        os.mkdir(texts_folder + "/" + sub + "/" + texts_lemma_folder)

    # Remove folder with old data
    for file in os.listdir(texts_folder + sub + "/" + normal_folder):
        os.remove(texts_folder + sub + "/" + normal_folder + file)

    for file in os.listdir(texts_folder + sub + "/" + texts_pos_folder):
        os.remove(texts_folder + sub + "/" + texts_pos_folder + file)

    for file in os.listdir(texts_folder + sub + "/" + texts_lemma_folder):
        os.remove(texts_folder + sub + "/" + texts_lemma_folder + file)

    # Create the normal txt files
    for key in list(texts.keys())[:max_users]:
        for i in range(len(texts[key])):
            text = texts[key][i]
            with open(texts_folder + sub + "/" + normal_folder + key + "_" + str(i), "w") as file:
                file.write(" ".join(text))

    # Create the POS tagged txt files
    for key in list(texts.keys())[:max_users]:
        for i in range(len(texts[key])):
            text = texts[key][i]
            with open(texts_folder + sub + "/" + texts_pos_folder + key + "_" + str(i), "w") as file:
                file.write(" ".join(map(lambda p: p[0], pos_tag(text))))

    # Create the lemmatized txt files
    lemmatizer = WordNetLemmatizer()

    for key in list(texts.keys())[:max_users]:
        for i in range(len(texts[key])):
            text = texts[key][i]
            with open(texts_folder + sub + "/" + texts_lemma_folder + key + "_" + str(i), "w") as file:
                file.write(" ".join(map(lemmatizer.lemmatize, text)))

    # Create the split configuration file for SuperStyl. It is the files that is used by SuperStyl to know which files to use
    # for training and for testing. This allows us to choose exactly the training and testing data
    generate_split(pair, texts_folder + sub + "/")

# Generates file for a pair of Subreddits
def generate_txt_double(pair):

    folder_name = "_".join(pair)
    # Load the texts
    with open("pairs/" + folder_name + "/" + pair[0] + ".json", "r") as file:
        texts_1 = json.load(file)
    
    with open("pairs/" + folder_name + "/" + pair[1] + ".json", "r") as file:
        texts_2 = json.load(file)

    # Create folders that do not exist
    if not os.path.exists(texts_folder + folder_name):
        os.mkdir(texts_folder + folder_name)

    if not os.path.exists(texts_folder + folder_name + "/" + normal_folder):
        os.mkdir(texts_folder + folder_name + "/" + normal_folder)

    if not os.path.exists(texts_folder + folder_name + "/" + texts_pos_folder):
        os.mkdir(texts_folder + folder_name + "/" + texts_pos_folder)

    if not os.path.exists(texts_folder + folder_name + "/" + texts_lemma_folder):
        os.mkdir(texts_folder + "/" + folder_name + "/" + texts_lemma_folder)

    # Remove folder with old data
    for file in os.listdir(texts_folder + folder_name + "/" + normal_folder):
        os.remove(texts_folder + folder_name + "/" + normal_folder + file)

    for file in os.listdir(texts_folder + folder_name + "/" + texts_pos_folder):
        os.remove(texts_folder + folder_name + "/" + texts_pos_folder + file)

    for file in os.listdir(texts_folder + folder_name + "/" + texts_lemma_folder):
        os.remove(texts_folder + folder_name + "/" + texts_lemma_folder + file)

    len_1 = len(texts_1[list(texts_1.keys())[0]])
    len_2 = len(texts_2[list(texts_2.keys())[0]])

    # Use the users that are in both Subreddits
    if len_1 > len_2:
        length = len_1
    else:
        length = len_2

    # Create the normal txt files
    for key in list(texts_1.keys())[:max_users]:
        for i in range(length):
            text_1 = texts_1[key][i]
            with open(texts_folder + folder_name + "/" + normal_folder + key + "_" + str(i), "w") as file:
                file.write(" ".join(text_1))
            text_2 = texts_2[key][i]
            with open(texts_folder + folder_name + "/" + normal_folder + key + "_" + str(length + i), "w") as file:
                file.write(" ".join(text_2))

    # Create the POS tagged txt files
    for key in list(texts_1.keys())[:max_users]:
        for i in range(length):
            text_1 = texts_1[key][i]
            with open(texts_folder + folder_name + "/" + texts_pos_folder + key + "_" + str(i), "w") as file:
                file.write(" ".join(map(lambda p: p[0], pos_tag(text_1))))
            text_2 = texts_2[key][i]
            with open(texts_folder + folder_name + "/" + texts_pos_folder + key + "_" + str(length + i), "w") as file:
                file.write(" ".join(map(lambda p: p[0], pos_tag(text_2))))

    # Create the lemmatized txt files
    lemmatizer = WordNetLemmatizer()

    for key in list(texts_1.keys())[:max_users]:
        for i in range(length):
            text_1 = texts_1[key][i]
            with open(texts_folder + folder_name + "/" + texts_lemma_folder + key + "_" + str(i), "w") as file:
                file.write(" ".join(map(lemmatizer.lemmatize, text_1)))
            text_2 = texts_2[key][i]
            with open(texts_folder + folder_name + "/" + texts_lemma_folder + key + "_" + str(length + i), "w") as file:
                file.write(" ".join(map(lemmatizer.lemmatize, text_2)))

    # Create the split configuration file for SuperStyl. It is the files that is used by SuperStyl to know which files to use
    # for training and for testing. This allows us to choose exactly the training and testing data which in this case is important
    # for the topic confusion test
    generate_split_double(pair, texts_folder + folder_name + "/", length)
    generate_split_confusion(pair, texts_folder + folder_name + "_confusion/", length)


if __name__ == "__main__":
    if not os.path.isdir(texts_folder):
        os.mkdir(texts_folder)
        
    for pair in pairs:
        for sub in pair:
            generate_txt_single(sub, "_".join(pair))

        generate_txt_double(pair)
