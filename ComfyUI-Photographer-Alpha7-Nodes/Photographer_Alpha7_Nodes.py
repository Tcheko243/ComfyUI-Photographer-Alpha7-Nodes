"""
developed by: Dimonapatrick243
day: 2024 06 20

"""



import webbrowser
import os
import json
import random
import csv
import cv2
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

class PA7_Comfy_Viewer:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "view_image"
    CATEGORY = "PA7/Utility"

    # Créez le dossier temporaire dans le même répertoire que ce fichier Python
    script_dir = os.path.dirname(__file__)
    temp_dir = os.path.join(script_dir, "temp")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    image_path = os.path.join(temp_dir, "output_image.png")
    info_path = os.path.join(temp_dir, "image_info.txt")
    viewer_url = None  # Stocker l'URL du visualiseur

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",)
            }
        }

    def extract_metadata(self, image_path):
        # Ouvrir l'image pour extraire les métadonnées
        with Image.open(image_path) as img:
            metadata = img.info

        # Extraire les informations pertinentes des métadonnées
        prompt = metadata.get("prompt", "N/A")
        width = metadata.get("width", "N/A")
        height = metadata.get("height", "N/A")
        sampler = metadata.get("sampler", "N/A")

        # Enregistrer les informations des métadonnées dans un fichier texte
        with open(self.info_path, "w") as info_file:
            info_file.write(f"Prompt: {prompt}\n")
            info_file.write(f"Width: {width}px\n")
            info_file.write(f"Height: {height}px\n")
            info_file.write(f"Sampler: {sampler}\n")

    def create_dynamic_css(self):
        css_content = """
        body {
            background-color: #2b2b2b; /* Changez cette couleur de fond */
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
        }
        img {
            max-width: 90%;
            max-height: 80vh;
            border: 1px solid #ff0000;
        }
        .metadata {
            margin-top: 20px;
        }
        .metadata h2 {
            margin-bottom: 10px;
        }
        .metadata p {
            margin: 5px 0;
        }
        """
        css_path = os.path.join(PA7_Comfy_Viewer.temp_dir, "dynamic_style.css")
        with open(css_path, "w") as css_file:
            css_file.write(css_content)
        return css_path

    def view_image(self, image):
        # Convertir l'image en tableau numpy et vérifier les dimensions
        image_array = np.array(image)

        # Vérifier les dimensions de l'image
        print(f"Image original shape: {image_array.shape}")

        # Si l'image a 4 dimensions, supprimer la première dimension
        if len(image_array.shape) == 4 and image_array.shape[0] == 1:
            image_array = np.squeeze(image_array, axis=0)
            print(f"Squeezed image shape: {image_array.shape}")

        # Vérifier les dimensions de l'image
        if len(image_array.shape) == 3:
            height, width, channels = image_array.shape
            print(f"Image dimensions: {width}x{height}, Channels: {channels}")
        elif len(image_array.shape) == 2:
            height, width = image_array.shape
            print(f"Image dimensions: {width}x{height}, Grayscale")
        else:
            print("Unsupported image shape:", image_array.shape)
            return (image,)

        if width > 10000 or height > 10000:
            print(f"Image dimensions exceed limit: {width}x{height}")
            return (image,)

        # Convertir l'image en format BGR pour cv2 si elle est en RGB
        if channels == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Convertir les valeurs des pixels en entiers appropriés
        image_array = np.clip(image_array * 255, 0, 255).astype(np.uint8)

        # Afficher quelques valeurs de pixels pour déboguer
        print("Pixel values at (0, 0):", image_array[0, 0])

        success = cv2.imwrite(self.image_path, image_array)
        if not success:
            print(f"Failed to write image to {self.image_path}")
            return (image,)

        print(f"Image successfully written to {self.image_path}")

        # Extraire les métadonnées et les enregistrer dans un fichier
        self.extract_metadata(self.image_path)

        # Créer le fichier CSS dynamique
        css_path = self.create_dynamic_css()

        # Ouvrir le visualiseur HTML (une seule fois)
        viewer_path = os.path.join(os.path.dirname(__file__), "viewer_v2.html")
        viewer_url = f"file://{viewer_path}"

        if PA7_Comfy_Viewer.viewer_url != viewer_url:
            webbrowser.open(viewer_url)
            PA7_Comfy_Viewer.viewer_url = viewer_url

        # Retourner l'image au prochain nœud du pipeline
        return (image,)

class PA7_Negative_Prompt():
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_negative_tags"
    CATEGORY = "PA7/Utility"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "option": (["UnRealistic", "AnimNegative"],)
            }
        }

    def get_negative_tags(self, option):
        tags = {
            "PA7_UnRealistic": "3d, cgi, cartoon, sketch, drawing, illustration, manga, anime, digital art, painting, airbrushed, glitch, ugly, nude, nsfw, naked, bad hands, fake, blurry, signature, watermark, text",
            "PA7_AnimNegative": "bad anatomy, blurry, bad proportions, cropped, disfigured, low quality, out of frame, watermark, jpeg artifacts"
        }
        return (tags.get(option, ""),)

class PA7_Prompt_Generator:
    RETURN_TYPES = ("STRING", "STRING")
    FUNCTION = "generate_prompts"
    CATEGORY = "PA7/Utility"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_file_path": ("STRING",)
            }
        }

    def load_elements_from_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def generate_prompt(self, elements):
        opening_phrase = random.choice(elements['opening_phrases'])
        subject = random.choice(elements['subjects'])
        hair_style = random.choice(elements['hair_styles'])
        hair_color = random.choice(elements['hair_colors'])
        clothing_style = random.choice(elements['clothing_styles'])
        collar = random.choice(elements['collars'])
        accessory = random.choice(elements['accessories'])
        expression = random.choice(elements['expressions'])
        ambiance = random.choice(elements['ambiances'])
        lighting = random.choice(elements['lightings'])
        background = random.choice(elements['backgrounds'])

        prompt = f"{opening_phrase} {subject} {hair_style} and {hair_color}, wearing {clothing_style} with {collar}, {accessory}, {expression}."
        completion = f"{ambiance}. {lighting}. {background}."

        return prompt, completion

    def generate_prompts(self, json_file_path):
        elements = self.load_elements_from_json(json_file_path)
        prompt, completion = self.generate_prompt(elements)
        return (prompt, completion,)
    
NODE_CLASS_MAPPINGS = {
    "PA7_Comfy_Viewer": PA7_Comfy_Viewer,
    "PA7_Negative_Prompt": PA7_Negative_Prompt,
    "PA7_Prompt_Generator": PA7_Prompt_Generator

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PA7_Comfy_Viewer": "PA7 Comfy Viewer",
    "PA7_Negative_Prompt": "PA7 Negative Prompt",
    "PA7_Prompt_Generator": "PA7 Prompt Generator"

}



