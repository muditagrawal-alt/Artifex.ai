import requests
from PIL import Image
from io import BytesIO
import os
import json
import base64
from IPython.display import display

#CONFIGURING THE API FROM STABILITY.AI:
API_KEY = "sk-tKQbaZNPSrCINZV4kmEsIvGL3iNAjiwNIiu0c0uDTKRTOM12"
url_template = "https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
os.makedirs("images", exist_ok=True)

#FUNCTION FOR GENERATING IMG:
def generate_image(prompt, engine_id, aspect_ratio="1:1", seed=None, output_dir="images"):
    data = {"text_prompts": [{"text": prompt}], "aspect_ratio": aspect_ratio}
    if seed is not None:
        data["seed"] = seed

    url = url_template.format(engine_id=engine_id)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if "artifacts" in result and result["artifacts"]:
            img_base64 = result["artifacts"][0]["base64"]
            img = Image.open(BytesIO(base64.b64decode(img_base64)))
            filename = f"{output_dir}/{prompt.replace(' ', '_')}.jpeg"
            img.convert("RGB").save(filename, format="JPEG", quality=95)
            return filename, img
        else:
            print("Error: No artifacts found.")
            return None, None
    else:
        print("API Response:", response.text)
        raise Exception(f"Error: {response.status_code}")

#MAIN EXECUTION FOR IMG GEN:
user_prompt = input("Enter your prompt: ")  # e.g., "generate an image of a car"
engine_id = "stable-diffusion-v1-6"

filename, image = generate_image(user_prompt, engine_id, "16:9")

if filename and image:
    display(image)  # Displays the image right in the notebook
    print(f"Image saved as: {filename}")
else:
    print("Image generation failed.")
