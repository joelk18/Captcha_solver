#from skimage.transform import resize
#import skimage
import os
#import numpy as np
#import re
directory = "setons"
start_at = 201
#pattern = "r\b[a-zA-Z0-9]+(?=\.)"
with open("new_data_set.txt", "w") as file_txt:
    for root, dirs, files in os.walk(directory):
        for element, file in enumerate(files):
            image_path = os.path.join(root, file)
            #rename the file
            new_file_name = f"captcha_image_{element}.png"
            new_image_path = os.path.join(root, new_file_name)
            os.rename(image_path, new_image_path)
            #image = skimage.io.imread(image_path)
            #print(image.shape)
            #image = resize(image, (75, 250, 3))
            #image = (image * 255).astype(np.uint8)
            #caracters_in_image = re.findall(pattern, file)
            #file_upper = file.upper()
            #print(file_upper[:5])
            #skimage.io.imsave(f"train_dataset/captcha_image_{start_at}.png", image)
            #start_at += 1
            file_txt.write(file[:-4])
            file_txt.write("\n")
            #if start_at % 200 == 0:
            #    print(file_upper[:5])