from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
import requests
img_name = "captchaFR_CaptchaImage"
# Configurer Selenium avec le WebDriver (ex. Chrome)
for i in range(301, 401):
    driver = webdriver.Firefox()
    time.sleep(2)
    # Accéder à la page contenant le captcha
    driver.get("https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/4382/cgu/")

    # Localiser l'image captcha
    captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "captchaFR_CaptchaImage")))
    #captcha_url = captcha_element.get_attribute("src")  # URL de l'image captcha

    # Utiliser JavaScript pour extraire les données de l'image `blob:`
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
    with open(f"images_from_sous_pref/{i}.png", "wb") as file:
        file.write(base64.b64decode(captcha_base64))
        print(i)
    


    driver.quit()
