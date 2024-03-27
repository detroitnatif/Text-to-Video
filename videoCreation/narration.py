import playsound
import os
import openai
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

def parse(narration):
    output = []
    paragraphs = narration.split('\n')
    print('paragraphs ', paragraphs)
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
    
    print()
    print("output  ", output)
    return output
    
def create(data, output_file):
    narration = ''
    for element in data:
        if element['type'] != 'text':
            continue
        narration += element['content'] + '\n\n'
    print('narration ',  narration)
    audio = openai.audio.speech.create(
        input=narration,
        model='tts-1',
        voice='alloy'
    )
    audio.stream_to_file(output_file)
    # playsound.playsound('audio.mp3')
    # os.remove('audio.mp3')