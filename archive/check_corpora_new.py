import json
import os

from utils import words_regex, texts_len

dir = "amt/"
filter_list = ["demographic", "imitation", "obfuscation", "verification"]

texts = {}

for d in os.listdir(dir):
    name_dir = dir + d
    if os.path.isdir(name_dir):
        name = d
        user_texts = []
        for file in os.listdir(name_dir):
            if any(map(lambda s: s in file, filter_list)):
                print("removed: " + file)
                os.remove(name_dir + "/" + file)
            else:
                if len(user_texts) == 10:
                    with open(name_dir + "/" + file, "r") as file:
                        text = " ".join(file.readlines())                    
                        user_texts.append(words_regex.findall(text)[:texts_len])
        texts[d] = user_texts

with open("test_texts.json", "w+") as file:
    json.dump(texts, file, indent=4)
