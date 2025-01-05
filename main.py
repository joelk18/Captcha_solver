from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import base64
import requests
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

link_1 = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/2381/cgu/"
link_0 = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/4382/cgu/"
#Environment variables loading
load_dotenv()

#email configuration
expediteur = os.getenv("EMAIL_EXPEDITEUR")
mot_de_passe = os.getenv("EMAIL_PASSWORD")
destinataire = os.getenv("EMAIL_DESTINATAIRE")
# GMX SMTP Server details
SMTP_SERVER = 'mail.gmx.com'
SMTP_PORT = 465

img_name = "captchaFR_CaptchaImage"

#model loading
model_v0 = VisionEncoderDecoderModel.from_pretrained("./model_save/model_trocr_finetuned_v0")
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")

#Selenium configuration
driver = webdriver.Firefox()
time.sleep(2)
#going to the website with the captcha
driver.get(link_1)

#Locate the image 
captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captchaFR_CaptchaImage")))
#captcha_url = captcha_element.get_attribute("src")  # URL de l'image captcha

# extract the image `blob:`
captcha_base64 = driver.execute_script("""
            const img = arguments[0];  // Obtenez l'élément <img>
            const canvas = document.createElement('canvas'); // Créez un canvas HTML5
            canvas.width = img.naturalWidth;  // Largeur réelle de l'image
            canvas.height = img.naturalHeight;  // Hauteur réelle de l'image
            const ctx = canvas.getContext('2d'); // Contexte 2D pour dessiner
            ctx.drawImage(img, 0, 0);  // Dessinez l'image sur le canvas
            return canvas.toDataURL('image/png').split(',')[1];  // Extraire les données en Base64
        """, captcha_element)

    # Convertir les données Base64 en un fichier image
with open(f"live_captchat/image.png", "wb") as file:
    file.write(base64.b64decode(captcha_base64))

# Load the image
image = Image.open(f"live_captchat/image.png").convert("RGB")
# Preprocess the image
pixel_values = processor(image, return_tensors="pt").pixel_values
generated_ids = model_v0.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(generated_text)
# Fill the captcha
captcha_input = driver.find_element(By.ID, "captchaFormulaireExtInput")
captcha_input.send_keys(generated_text)
time.sleep(5)
# Submit the form
suivant = driver.find_element(By.CSS_SELECTOR, "button.q-btn.q-btn--standard.q-btn--actionable")
suivant.click()
time.sleep(2)
#repeat the process until the captcha is correct
while driver.current_url == link_1 + "?error=invalidCaptcha":
    captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captchaFR_CaptchaImage")))
    captcha_base64 = driver.execute_script("""
            const img = arguments[0];  // Obtenez l'élément <img>
            const canvas = document.createElement('canvas'); // Créez un canvas HTML5
            canvas.width = img.naturalWidth;  // Largeur réelle de l'image
            canvas.height = img.naturalHeight;  // Hauteur réelle de l'image
            const ctx = canvas.getContext('2d'); // Contexte 2D pour dessiner
            ctx.drawImage(img, 0, 0);  // Dessinez l'image sur le canvas
            return canvas.toDataURL('image/png').split(',')[1];  // Extraire les données en Base64
        """, captcha_element)

    # Convertir les données Base64 en un fichier image
    with open(f"live_captchat/image.png", "wb") as file:
        file.write(base64.b64decode(captcha_base64))

    # Load the image
    image = Image.open(f"live_captchat/image.png").convert("RGB")
    # Preprocess the image
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model_v0.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_text)
    # Fill the captcha
    captcha_input = driver.find_element(By.ID, "captchaFormulaireExtInput")
    captcha_input.send_keys(generated_text)
    time.sleep(5)
    # Submit the form
    suivant = driver.find_element(By.CSS_SELECTOR, "button.q-btn.q-btn--standard.q-btn--actionable")
    suivant.click()
time.sleep(5)

#Look to see if there is a rendez-vous available
no_rendez_vous = True
while no_rendez_vous:
    try:
        rendez_vous = driver.find_element(By.XPATH, "//*[text()='Choisissez votre créneau']")

        # Création du message
        subject = "Alert rendez-vous available"
        body_message = "Bonjour,\n\nRendez-vous disponible pour la préfecture !!.\n\nCordialement."
        message = MIMEMultipart()
        message["From"] = expediteur
        message["To"] = destinataire
        message["Subject"] = subject
        message.attach(MIMEText(body_message, "plain"))
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as serveur:
                serveur.set_debuglevel(1)
                serveur.login(expediteur, mot_de_passe)
                serveur.sendmail(expediteur, destinataire, message.as_string())
            no_rendez_vous = False
            print("E-mail send with success !")
        except Exception as e:
            print(f"E-mail not send : {e}")
    except NoSuchElementException:
        print("No rendez-vous available")
        driver.refresh()
        time.sleep(2)
        no_rendez_vous = True
        continue
driver.close()
driver.quit()
