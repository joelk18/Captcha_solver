import os
import shutil
import re
import matplotlib.pyplot as plt
from PIL import Image
import time
directory = "images_from_sous_pref"
start_at = 201
dico_temp = {}
#pattern = "r\b[a-zA-Z0-9]+(?=\.)"
for root, dirs, files in os.walk(directory):
    for file in files:
           number = re.findall(r'\d+', file)[0]
           dico_temp[int(number)] = file
#print(dico_temp)
#plt.figure(figsize = (40, 40))
with open("values_captchat.txt", "r") as file_txt:
        for i in range(len(dico_temp)):
            txt = str(file_txt.readline())[:-1]
            shutil.copy(directory + "/"+ dico_temp[i], f"data_ocr/{txt}.png")
            #print(f"{txt}: {i}")
#           time.sleep(1)
#           img = Image.open(f"data_ocr/{txt}.png")
#           plt.subplot(20, 21, i+1)
#           plt.imshow(img)
#           plt.title(txt)
            #if i ==120:
            #    break
#plt.show()
#print(dico_temp)