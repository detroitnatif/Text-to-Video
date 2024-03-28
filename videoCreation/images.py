from openai import OpenAI
import os
from dotenv import load_dotenv
import narration
import json
import base64

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def create_from_data(data):
    image_num = 0
    for element in data:
        if element['type'] != 'image':
            continue
        image_num += 1
        image_name = f'image_{image_num}.webp'
        generate(element['description'], os.path.join('images', image_name))

def generate(prompt="POV like youve got a GoPro on looking down while cutting cutting an onion", output_file='creation.webp'):
    response =  client.images.generate(
        model='dall-e-3',
        prompt='create POV images as if you were doing the action looking down ' + prompt,
        size='1024x1024',
        quality='standard',
        n=1,
        response_format='b64_json')

    image_b64 = response.data[0].b64_json

    with open(output_file, 'wb') as f:
        f.write(base64.b64decode(image_b64))
    # return output_file
