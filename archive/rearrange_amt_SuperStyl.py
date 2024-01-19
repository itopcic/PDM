import json
import os
import shutil

from utils import words_regex

dir = "amt/"
filter_list = ["demographic", "imitation", "obfuscation", "verification"]
filter_dir = ["test", "train"]

if not os.path.exists("amt/superstyl"):
    os.mkdir("amt/superstyl")

for d in os.listdir(dir):
    name_dir = dir + d
    if os.path.isdir(name_dir) and d not in filter_dir:
        user_texts = []
        for file in os.listdir(name_dir):
            if any(map(lambda s: s in file, filter_list)):
                print("removed: " + file)
                os.remove(name_dir + "/" + file)
            else:
                shutil.copy(name_dir + "/" + file, "amt/superstyl/")
