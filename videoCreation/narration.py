import playsound
import os
import openai
import warnings
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream, save
import subprocess
import random
import requests

warnings.filterwarnings("ignore", category=DeprecationWarning)

elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")

narration_api = 'openai' # 'elevenlabs'


client = ElevenLabs(
  api_key=elevenlabs_key
)

def parse(narration):
    output = []
    paragraphs = narration.split('\n')

    for paragraph in paragraphs:
        if paragraph.startswith("Narrator: "):
            text = paragraph.replace("Narrator: ", '')
            output.append(
                {'type': 'text',
                 'content': text}
            )
        elif 'Background image:' in paragraph:
            # Splitting by ':' to accurately remove the "[Background image:" part and the trailing ']'
            # This also handles removing any leading enumeration like "1) [" by splitting and taking the last part
            background = paragraph.split(': ', 1)[-1].rstrip(']')
            output.append(
                {'type': 'image',
                 'description': background}
            )
    
    return output
    
def create(data, output_file):
    narration = ''
    for element in data:
        if element['type'] != 'text':
            continue
        narration += element['content'] + '\n\n'
  
    if narration_api == 'openai':
        audio = openai.audio.speech.create(
            input=narration,
            model='tts-1',
            voice='alloy'
        )
        audio.stream_to_file(output_file)
    else:
        audio = client.generate(
            text=narration,
            voice='Grace'
        
        )
        play(audio)
        save(audio, output_file)
