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

# prompt = input("prompt: ")

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
                    'text': 'what does this page include, make sure to include personal details like age?'
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
    messages=[
        {
            "role": "assistant",
            'content': image_description
        },

        {
            'role': 'user',
            'content': 'using only the data given to you, how old is sam altman?'
        }
    ]
)

# Print the GPT-3.5 model's response to the specific question
print("GPT-3.5 Response:", response_gpt3_turbo.choices[0].message.content)
