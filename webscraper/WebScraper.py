from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
import json
import subprocess
from PIL import Image
import io


load_dotenv()
model = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def resize_and_compress_image(image_path, output_size=(500, 350), quality=75):
    """
    Resize and compress an image, then encode it in base64.

    :param image_path: Path to the input image.
    :param output_size: A tuple (width, height) to resize the image.
    :param quality: Quality of the output JPEG image (1-100).
    :return: Base64-encoded string of the resized and compressed image.
    """
    with Image.open(image_path) as img:
        img = img.resize(output_size, Image.ANTIALIAS)
        with io.BytesIO() as buf:
            img.save(buf, format='JPEG', quality=quality)
            byte_data = buf.getvalue()
    return base64.b64encode(byte_data).decode()
    
prompt = input("prompt: ")
# Fixed: Removed the comma to prevent tuple creation
message_to_gpt = [
    {
        "role": "system",
        'content': "You are a web crawler, your job is to give a url to go to in order to find the answer to the question. Respond in the following JSON format{\"url\": \"<put url here>\"}"
    },
    {
        'role': 'user',
        'content': prompt
    }
]

while True:
    response_url_gpt3_turbo = model.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=message_to_gpt,
        max_tokens=300,
        response_format={'type': 'json_object'}
    )

    print('crawling: ', response_url_gpt3_turbo.choices[0].message.content)

    response_json = json.loads(response_url_gpt3_turbo.choices[0].message.content)
    url = response_json['url']
    
    try:
        # Run the subprocess with a timeout
        result = subprocess.run(['node', 'screenshot.mjs', url], timeout=30)
        print('result', result)
    
        if result.returncode != 0:
            print('failed')
            raise Exception("Subprocess failed")
        break  # Exit the loop if successful
    except subprocess.TimeoutExpired:
        print('timed out')
    except Exception as e:
        print(f"Error: {e}")
        # Append failure message and prompt for a different URL
        message_to_gpt.append(
            {'role': 'user',
             'content': 'I was unable to crawl that site, please pick a different URL'}
        )

b64_image = resize_and_compress_image("screenshot.jpg")


# Correcting the structure for GPT-4 Vision's request
response_gpt4_vision = model.chat.completions.create(
    model='gpt-4-vision-preview',
    messages=[
        {
            'role': 'system',
            'content': 'your job is to answer the users question based on the image given, if you cant find the answer in the image, respond just "ANSWER_NOT_FOUND"'
        },
        {
            'role': 'user',
            'content': [
             {   
                'type': 'image_url',
                'image_url': f"data:image/jpeg;base64,{b64_image}",
            
            },
            {
                'type': 'text',
                'text': prompt,
            },]
        }
        
    ],
    max_tokens=1024
)


# Assuming this is your intended logic for handling the response
if response_gpt4_vision.choices:
    if "ANSWER_NOT_FOUND" in response_gpt4_vision.choices[0].message.content:
        print("ANSWER NOT FOUND")
        message_to_gpt.append({
            'role': 'user',
            'content': 'i was unable to find the answer on that website, pick another one'
        })
        
    else:
        image_description = response_gpt4_vision.choices[0].message.content
        print('image description:', image_description)
