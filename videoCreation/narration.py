def create(narration):
    paragraphs = narration.split('\n')
    for paragraph in paragraphs:
        if paragraph.startswith("Narrator: "):
            text = paragraph.replace("Narrator: ", '')
            print(f'text: {text}')
        elif paragraph.startswith('['):
            background = paragraph.replace('Background Image: ', '')
            print(f'background: {background}')

       