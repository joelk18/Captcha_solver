import os
import google.generativeai as genai
import PIL.Image
API_KEY = "AIzaSyACG3K8YmlqxmPOuIxXBm1NfsRj0kq2tuA"
genai.configure(api_key=API_KEY)

#Select images
images = []
for i in range(351, 401):
    image_path = f"images_from_sous_pref/{i}.png"
    image = PIL.Image.open(image_path)
    images.append(image)
#image_path = "images_from_sous_pref/2.png"
#image = PIL.Image.open(image_path)
#Get the text from the image
prompt = "Give me only the text from the image no more for each image."
prompt_images = [prompt] + images
#Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro")


response = model.generate_content(prompt_images)
#save the text in a file
with open("new_ds_maybe.txt", "a") as file_txt:
    file_txt.write("\n")
    file_txt.write(response.text)
print(response.text)