from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv




load_dotenv()


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


import requests
import os
import simpleaudio as sa

# Assuming 'result.choices[0].message.content' contains the text you want to convert to speech

PROMPT_MESSAGES = [
    {
        'role': 'user',
        'content': "tell me that everything is going to be alright but do it with a jamaiacan patois sounding like bob marley"
    }
]

params = {
    "model": "gpt-3.5-turbo",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 500,
}


result = client.chat.completions.create(**params)
print(result)

response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
    },
    json={
        "model": "tts-1-1106",
        "input": result.choices[0].message.content,  
        "voice": "onyx",
    },
)

import pygame
import requests
import os

# Assuming 'response' is obtained from the OpenAI API as shown previously

# Check if the request was successful
if response.status_code == 200:
    audio = b""
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        audio += chunk

    # Save the audio content to an MP3 file
    audio_file_path = 'output_audio.mp3'
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio file and play it
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

else:
    print(f"Error: {response.status_code}")
    print(response.text)

