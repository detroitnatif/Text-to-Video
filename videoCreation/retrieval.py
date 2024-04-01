from openai import OpenAI
import os
from dotenv import load_dotenv
import json


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")

narration_api = 'openai' # 'elevenlabs' 

user_input = input("what would you like to eat?: ")

response =  client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {
            'role':'system',
            'content': ''' Your job is to give recipe with clear and straigtforward steps. Skip the thematic answers and just give numbered steps.
            '''
        },
        {
            'role': 'user',
            'content': f'create a Youtube Short narration based for the following {user_input}, emphasizing the exact steps of the recipe: '
        }
    ]

)
response = response.choices[0].message.content
print(response)