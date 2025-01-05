from captcha.image import ImageCaptcha
import random
import string

# Générateur de texte personnalisé
def generate_random_text(length=9, characters="ECB9AX68Y5K4PNMT3JWRHVUDSILG0OF"):#string.ascii_uppercase + string.digits):
    return ''.join(random.choices(characters, k=length))


for i in range(500):
    # Création d'un CAPTCHA avec des paramètres personnalisés
    image = ImageCaptcha(
        width=250,
        height=75,
        fonts=['C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/Calibri.ttf', 'C:/Windows/Fonts/Century.ttf', 'C:/Windows/Fonts/Corbel.ttf'],#'
        font_sizes=[100, 105, 110]
    )

    # Génération du texte et de l'image
    captcha_text = generate_random_text(length=random.randint(7, 9))
    image_file = f"test_ds_gen/{captcha_text}.png"
    image.write(captcha_text, image_file)

    #print(f"CAPTCHA personnalisé généré : {image_file}")
