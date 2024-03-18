from openai import OpenAI
import base64
from dotenv import load_dotenv
import os


load_dotenv()
model = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def image_b64(image):
    with open(image, 'rb') as f:
        return base64.b64encode(f.read()).decode()

b64_image = image_b64("screenshot.jpg")



response = model.chat.completions.create(model='gpt-4-vision-preview',
    messages=[
        {
            'role': 'user',
            'content': [
                {
                    'type':"image_url",
                    'image_url': f"data:image/jpeg;base64, {b64_image}",
                },
                {
                    'type': 'text',
                    'text': 'what is in this image?'
                }
            ]
        }
    ]
    )
message_text = response.choices[0].message.content
print(message_text)