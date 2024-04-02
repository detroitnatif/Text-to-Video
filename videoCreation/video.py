import cv2
import os
import glob
import numpy as np
import math
import subprocess
from pydub import AudioSegment
import json
import text

def get_audio_duration(audio_file):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Calculate the length in milliseconds
    length_in_milliseconds = len(audio)

    
    return length_in_milliseconds

def images_to_video(image_folder, avi_video_name, output_file, data_json, fps=30 ):
    """
    Combines images from a folder into a video, applying a blending effect between images.

    Parameters:
    - image_folder: Path to the folder containing the images.
    - avi_video_name: The image video without audio (including path and extension).
    - fps: Frames per second for the output video.
    - output_file: Where mp4 video is saved.
    """
    wait_time = 1000
    width, height = 1024, 1792
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(avi_video_name, fourcc, fps, (width, height))

    # Sort images to ensure correct order
    image_paths = sorted(os.listdir(image_folder))
    full_narration = AudioSegment.empty()

    text_items = [item["content"] for item in data_json if item["type"] == "text"]
    
    

    for i, img in enumerate(image_paths):
        image1 = cv2.imread(os.path.join(image_folder, image_paths[i]))

        if i < len(image_paths) - 1:
            image2 = cv2.imread(os.path.join(image_folder, image_paths[i + 1]))
        else:
            image2 = cv2.imread(os.path.join(image_folder, image_paths[0]))

        # Ensure the images are resized or cropped to fit the video dimensions
        image1 = cv2.resize(image1, (width, height))
        image2 = cv2.resize(image2, (width, height))

        narration = os.path.join('narration', f'narration_{i+1}.mp3')
        full_narration += (AudioSegment.from_file(narration))
        duration = get_audio_duration(narration) 

        frames_for_image = int((duration / 1000) * fps) - fps
        
        text_items = [item["content"] for item in data_json if item["type"] == "text"]
        for _ in range(frames_for_image):
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = image1

            text_no_quotes = text_items[i].strip('"')
            bullet_points = text_no_quotes.split('. ')
            bullet_points = [point for point in bullet_points if point]  # Remove any empty strings
            formatted_text = '\n'.join(f"\n- {point}" if not point.endswith('.') else f"\n- {point[:-1]}" for point in bullet_points)

            text.write_text(formatted_text,vertical_video_frame)

            video.write(vertical_video_frame)

        fade_duration_frames = min(frames_for_image, fps)  
        for alpha in np.linspace(0, 1, fade_duration_frames):
            blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            video.write(blended_image)

    full_narration.export('full_narration.mp3', format='mp3')

    video.release()
    ffmpeg_command = ['ffmpeg', '-i', avi_video_name, '-i', 'full_narration.mp3', '-map', '0:v', '-map', '1:a', '-c:v', 'copy','-c:a', 'aac', '-strict', '-experimental', '-shortest', output_file]

    subprocess.run(ffmpeg_command)
    os.remove(avi_video_name)

# Example usage
    
file_path = '/Users/tylerklimas/Desktop/openaisandbox/videoCreation/data.json'

# Open the file for reading
with open(file_path, 'r') as file:
    # Load the JSON data from the file
    data_json = json.load(file)



images_folder = 'images'  # Ensure this is the correct path to your images
video_name = 'cooking_video_china.avi'  # Specify the full name including extension
fps = 30  # Frames per second
mp4 = 'cooking_with_captions.mp4'
images_to_video(images_folder, video_name ,mp4,data_json, fps)




