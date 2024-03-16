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
    _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # Adjust quality as needed
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read.")


PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "Generate a description of the person and where and what they are doing being as specific as possible.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::500]),
        ],
    },
]
params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)


# Display frames
# for img in base64Frames:
#     display(Image(data=base64.b64decode(img.encode("utf-8"))))
#     time.sleep(0.025)  # Control the display rate of the frames

# Display first frame
# img = base64Frames[0]
# display(Image(data=base64.b64decode(img.encode("utf-8"))))


