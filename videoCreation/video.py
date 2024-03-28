import cv2
import os
import glob

def images_to_video(image_folder, video_name, fps=30):
    """
    Combines images from a folder into a video.

    Parameters:
    - image_folder: Path to the folder containing the images.
    - video_name: The output video file name (including path).
    - fps: Frames per second for the output video.
    """
    # Get all image paths
    image_paths = os.listdir('images') 
    images.sort()  # Sort the images by name

    # Extract the dimensions of the first image
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use 'XVID' if you prefer
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for image in images:
        video.write(cv2.imread(image))

    cv2.destroyAllWindows()
    video.release()

# Usage example
image_folder = 'path/to/your/images'  # Update this to the path where your images are stored
video_name = 'output_video.mp4'  # Specify the output video file name
fps = 24  # Frames per second of the output video

images_to_video(image_folder, video_name, fps)
