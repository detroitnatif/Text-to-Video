import cv2
import os
import glob
import numpy as np
import math
import subprocess


def images_to_video(image_folder, video_name, fade_time=2000):
    """
    Combines images from a folder into a video, applying a blending effect between images.

    Parameters:
    - image_folder: Path to the folder containing the images.
    - video_name: The output video file name (including path and extension).
    - fps: Frames per second for the output video.
    """
    wait_time = 2000
    width, height = 1024, 1792
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_name, fourcc, fade_time, (width, height))

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

        for alpha in np.linspace(0, 1, math.ceil(fade_time/1000 * 30)):
            blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
            video.write(blended_image)

    
    video.release()
    subprocess.run('ffmpeg', '-i', video, 'narration.mp3')

# Example usage
images_folder = 'images'  # Ensure this is the correct path to your images
video_name = 'cooking_video.avi'  # Specify the full name including extension
fade_time = 30  # Frames per second

images_to_video(images_folder, video_name, fade_time)


