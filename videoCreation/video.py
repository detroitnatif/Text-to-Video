import cv2
import os
import glob
import numpy as np
import math
import subprocess


def images_to_video(image_folder, avi_video_name, output_file, fps=30 ):
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

    for i in range(len(image_paths) - 1):
        image1 = cv2.imread(os.path.join(image_folder, image_paths[i]))
        image2 = cv2.imread(os.path.join(image_folder, image_paths[i + 1]))

        # Ensure the images are resized or cropped to fit the video dimensions
        image1 = cv2.resize(image1, (width, height))
        image2 = cv2.resize(image2, (width, height))

        for i in range(math.ceil(wait_time/1000 * 30)):
            vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
            vertical_video_frame[:image1.shape[0], :] = image1

            video.write(vertical_video_frame)

        for alpha in np.linspace(0, 1, int(fps * 10)):
            blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            video.write(blended_image)

    
    video.release()
    ffmpeg_command = ['ffmpeg', '-i', avi_video_name, '-i', 'narration.mp3', '-map', '0:v', '-map', '1:a', '-c:v', 'copy','-c:a', 'aac', '-strict', '-experimental', '-shortest', output_file]

    subprocess.run(ffmpeg_command)

# Example usage
images_folder = 'images'  # Ensure this is the correct path to your images
video_name = 'cooking_video.avi'  # Specify the full name including extension
fps = 30  # Frames per second
mp4 = 'cooking_with_audio.mp4'
images_to_video(images_folder, video_name ,mp4, fps)


