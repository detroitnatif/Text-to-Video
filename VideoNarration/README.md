<div align='center'>
  
## Using GPT4 Vision to narrate videos

  <img src="video.png" width="300" >

### Video transformed to frames

Using OpenCV, the frames are loaded and decoded into utf-8 so they are able to be passed to the GPT-4 Vision API.

```
video = cv2.VideoCapture("/Users/tylerklimas/Library/Mobile Documents/com~apple~CloudDocs/Downloads/final_60abf503206f6000593a7d9e_779630.mp4")

base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # Adjust quality as needed
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

```

### GPT-4 Vision Request

Every 500th frame is sent to the API and prompted for a description at the moment. This creates the illusion of video comprehension. In this particular implementation I use the narration style of David Attenborough, the nature documentary legend known for his elaborate descriptions.

```
PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames of a video. Create a short voiceover script in the style of David Attenborough. Only include the narration.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::500]),
        ],
    },
]
params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 500,
}

result = client.chat.completions.create(**params)
```

### TTS Narration

Using the created transcript, a request is sent to Open AI's text-to-speech API.

```

response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
    },
    json={
        "model": "tts-1-1106",
        "input": result.choices[0].message.content,  # Assuming you want to use the 'test' variable here
        "voice": "onyx",
    },
```

### Save and Play the response

Pygame processes and saves the response. Audio is played.

</div>
