import json
import os

from utils import words_regex, texts_len

dir = "amt/"
filter_list = ["demographic", "imitation", "obfuscation", "verification"]

texts = {}

for d in os.listdir(dir):
    if d != "test" and d != "train":
        name_dir = dir + d
        if os.path.isdir(name_dir):
            name = d
            user_texts = []
            for file in os.listdir(name_dir):
                if len(user_texts) == 10:
                    break
                if not any(map(lambda s: s in file, filter_list)):
                    with open(name_dir + "/" + file, "r") as file:
                        text = " ".join(file.readlines())                    
                        user_texts.append(words_regex.findall(text)[:texts_len])
            texts[d] = user_texts

with open("test_texts.json", "w+") as file:
    json.dump(texts, file, indent=4)

print(texts)