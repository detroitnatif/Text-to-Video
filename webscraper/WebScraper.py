from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
import json

load_dotenv()
model = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def image_b64(image):
    with open(image, 'rb') as f:
        return base64.b64encode(f.read()).decode()

b64_image = image_b64("screenshot.jpg")

prompt = input("prompt: ")
message_to_gpt = [
        {
            "role": "system",
            'content': "You are a web crawler, your job is to give a url to go to in order to find the answer to the question. Respond in the following JSON format{\"url\": \"<put url here>\"}"
        },

        {
            'role': 'user',
            'content': prompt
        }
    ],

response_gpt4_vision = model.chat.completions.create(model='gpt-4-vision-preview',
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
                    'text': 'what does this page include, make sure to include all details?'
                }
            ]
        }
    ],
    max_tokens=1024
    )


# Assuming response_gpt4_vision is the response from the first model providing an image description
image_description = response_gpt4_vision.choices[0].message.content
print('image description:  ', image_description)
# Now, formulate a new question that uses the image description as context
specific_question = f"Based on this description: \"{image_description}\", how old is he"

# Make the new query to GPT-3.5 with the specific follow-up question
response_gpt3_turbo = model.chat.completions.create(
    model='gpt-3.5-turbo',
    messages= message_to_gpt,
    max_tokens=300,
    response_format={'type': 'json_object'}
)

# Print the GPT-3.5 model's response to the specific question
print("GPT-3.5 Response:", response_gpt3_turbo.choices[0].message.content)
response_json = json.loads(response_gpt3_turbo.content)
url = response_json['url']
