import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from utils.AI_Output_Input import *

url = "http://127.0.0.1:7860"

def generateImageByStableDiffusion(prompt:str):
    payload = {
    "prompt": prompt,
    "seed": -1,
    "batch_size": 1,
    "batch_count": 1,
    "n_iter": 1,
    "steps": 50,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "negative_prompt": "nude",
    "send_images": True,
    "save_images": False,
    "sampler_index": "Euler",
    }

    speakByPytts("Wait, Generating Image")

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.show(pnginfo)

if __name__ == "__main__":
    generateImageByStableDiffusion(prompt="A boy killing her girlfriend!")