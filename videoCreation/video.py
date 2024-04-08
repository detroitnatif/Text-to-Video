import cv2
import os
import glob
import numpy as np
import math
import subprocess
from pydub import AudioSegment
import json
import text
import shutil

# Set the paths for ffmpeg and ffprobe
ffmpeg_path = "/usr/bin/ffmpeg"
ffprobe_path = "/usr/bin/ffprobe"

# Configure pydub to use the specified ffmpeg and ffprobe
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path



def get_audio_duration(audio_file):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Calculate the length in milliseconds
    length_in_milliseconds = len(audio)

    
    return length_in_milliseconds


def images_to_video(image_folder, avi_video_name, output_file, data_json, output_dir, name, fps=30):
    """
    Combines images from a folder into a video, applying a blending effect between images.

    Parameters:
    - image_folder: Path to the folder containing the images.
    - avi_video_name: The image video without audio (file name only, no path).
    - fps: Frames per second for the output video.
    - output_file: File name for the final mp4 video (no path).
    - output_dir: The directory where the output files will be saved.
    - data_json: JSON data containing text items for narration.
    """
    wait_time = 1000
    width, height = 1024, 1792
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    avi_video_path = os.path.join(name, avi_video_name)  # Changed line
    video = cv2.VideoWriter(avi_video_path, fourcc, fps, (width, height))  # Adjusted to use avi_video_path

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

        image1 = cv2.resize(image1, (width, height))
        image2 = cv2.resize(image2, (width, height))

        narration = os.path.join(name, 'narration', f'narration_{i+1}.mp3')  # Unchanged, assumes 'narration' is a subfolder in the current directory
        full_narration += AudioSegment.from_file(narration)
        duration = get_audio_duration(narration)

        frames_for_image = int((duration / 1000) * fps) - fps

        for _ in range(frames_for_image):
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = image1

            text_no_quotes = text_items[i].strip('"')
            # bullet_points = text_no_quotes.split('. ')
            # bullet_points = [point for point in bullet_points if point]  # Remove any empty strings
            # formatted_text = '\n'.join(f"\n- {point}" if not point.endswith('.') else f"\n- {point[:-1]}" for point in bullet_points)

            text.write_text(text_no_quotes,vertical_video_frame)

            video.write(vertical_video_frame)
        
        for alpha in np.linspace(0, 1, min(frames_for_image, fps)):
            blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            video.write(blended_image)

    full_narration_path = os.path.join(output_dir, 'full_narration.mp3')  # Changed line
    full_narration.export(full_narration_path, format='mp3')  # Adjusted to use full_narration_path

    video.release()

    output_file_path = os.path.join(output_dir, output_file)  # Changed line
    ffmpeg_command = ['ffmpeg', '-i', avi_video_path, '-i', full_narration_path, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-strict', '-experimental', '-shortest', output_file_path]  # Adjusted to use avi_video_path and output_file_path

    try:
        result = subprocess.run(ffmpeg_command, check=True)
        print("ffmpeg command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg command failed: {e}")
    if result.returncode:
        return name
    else:
        exit()
    # videos_folder_path = 'videoCreation/videos'
    # new_file_path = os.path.join(videos_folder_path, f"{name}.mp4")

# Copy the video file to the new location with the new filename
    # shutil.copy(output_file_path, new_file_path)

    # os.remove(avi_video_path) 
    



# # Example usage
    
# file_path = '/Users/tylerklimas/Desktop/openaisandbox/videoCreation/falafel/data.json'

# # Open the file for reading
# with open(file_path, 'r') as file:
#     # Load the JSON data from the file
#     data_json = json.load(file)



# images_folder = '/Users/tylerklimas/Desktop/openaisandbox/videoCreation/falafel/images'  # Ensure this is the correct path to your images
# video_name = 'cooking_video_falafel.avi'  # Specify the full name including extension
# output_dir = '/Users/tylerklimas/Desktop/openaisandbox/videoCreation/videos'
# fps = 30  # Frames per second
# name = 'falafel'
# mp4 = f'{name}.mp4'
# images_to_video(images_folder, video_name,mp4,data_json,output_dir,'falafel', fps)





