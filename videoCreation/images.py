from openai import OpenAI
import os
# from dotenv import load_dotenv
import narration
import json
import base64
import requests
import io
from PIL import Image

# load_dotenv()


def create_from_data(data, name, api_key="You must give an API key to use"):
    image_num = 0
    for element in data:
        if element['type'] != 'image':
            continue
        image_num += 1
        image_name = f'image_{image_num}.webp'
        generate(element['description'], os.path.join(name, 'images', image_name))
        if image_num == 5:
            break
def generate(prompt="POV like youve got a GoPro on looking down while cutting cutting an onion", output_file='creation.webp'):

    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"} 
    payload = {f"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    image_bytes = response.content

    with open(output_file, 'wb') as f:
        f.write(image_bytes)
        # return output_file



# WORKING LIVE APP

# def create_from_data(data, name, api_key="You must give an API key to use"):
#     image_num = 0
#     for element in data:
#         if element['type'] != 'image':
#             continue
#         image_num += 1
#         image_name = f'image_{image_num}.webp'
#         generate(element['description'], os.path.join(name, 'images', image_name), api_key=api_key)
#         if image_num == 5:
#             break


# def generate(prompt="POV like youve got a GoPro on looking down while cutting cutting an onion", output_file='creation.webp', api_key="You must give an API key to use"):
#     client = OpenAI(api_key=api_key)
#     response =  client.images.generate(
#         model='dall-e-2',
#         prompt='create POV images as if you were doing the action looking down doing the action from a height of 4 feet, in a realistic photo style ' + prompt,
#         size='1024x1024',
#         quality='standard',
#         n=1,
#         response_format='b64_json')

#     image_b64 = response.data[0].b64_json

#     with open(output_file, 'wb') as f:
#         f.write(base64.b64decode(image_b64))
#     # return output_file


