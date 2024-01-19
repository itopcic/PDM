import os
import shutil

dir_name = "amt/"


for dirr in os.listdir(dir_name):
    pathname = dir_name + "test/"
    if not os.path.exists(pathname):
        os.mkdir(pathname)

    pathname = dir_name + "train/"
    if not os.path.exists(pathname):
        os.mkdir(pathname)

    files = os.listdir(dir_name + dirr)
    for i in range(len(files)):
        file = files[i]
        full_path = dir_name + dirr + "/" + file
        if i < 3:
            pathname = dir_name + "test/" + dirr
            if not os.path.exists(pathname):
                os.mkdir(pathname)
            shutil.copy(full_path, pathname)
        else:
            pathname = dir_name + "train/" + dirr
            if not os.path.exists(pathname):
                os.mkdir(pathname)
            shutil.copy(full_path, pathname)