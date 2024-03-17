from openai import OpenAI

model = OpenAI()


def image_b64(image):
    with open(image, 'rb') as f:
        return base64.b64encode(f.read()).decode()


response = model.chat.completions.create(model='gpt-4-vision-preview',
    messages=[
        {
            'role': 'user',
            'content': [
                {
                    'type':"image_url",
                    'image_url': "data.base64,image/jpeg; {b64_image}"
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
