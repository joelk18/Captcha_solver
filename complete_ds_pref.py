import os
import shutil
directory = "setons"
dest_directory = "images_from_sous_pref"
i = 499
"""
with open("values_captchat.txt", "a") as file_txt:
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_txt.write("\n")
            file_txt.write(file[:-4])
            shutil.copy(directory + "/" + file, f"{dest_directory}/captcha_image_{i}.png")
            i += 1
"""
file = open("new_ds_maybe.txt", "r")
values = file.read()
for count, value in enumerate(values):
    shutil.copy(f"{directory}/{count + 1}.png",f"{dest_directory}/captcha_image_{i}.png" )
    i += 1