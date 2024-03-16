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

video = cv2.VideoCapture("/Users/tylerklimas/Library/Mobile Documents/com~apple~CloudDocs/Downloads/final_60abf503206f6000593a7d9e_779630.mp4")

base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read.")

