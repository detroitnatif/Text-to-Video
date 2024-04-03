import cv2
import numpy as np

def write_text(text, frame):
    import cv2  # Ensure cv2 is imported

    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    thickness = 2  # Adjust thickness for better visibility
    initial_font_scale = 1  # Start with a default font scale
    border = 5
    line_spacing = 10  # Space between lines

    # Dynamically adjust font scale to fit text
    font_scale = initial_font_scale
    max_width = frame.shape[1]
    max_height = frame.shape[0]

    # Split text into words
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        # Check if adding the next word exceeds line width
        test_line = f"{current_line} {word}".strip()
        text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
        if text_size[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)  # Add the last line

    # Calculate total text block height
    text_height_total = 0
    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        text_height_total += text_size[1] + line_spacing
    text_height_total -= line_spacing  # Remove extra space after the last line

    # Calculate the starting Y position so that the text appears in the bottom third of the frame
    # Adjust the calculation for the starting Y position to move the text block to the bottom third
    third_height = max_height * 2 // 3
    text_y_start = max(third_height, max_height - text_height_total - border)  # Ensure text block starts within the bottom third

    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
        text_x = (max_width - text_size[0]) // 2
        text_y = text_y_start + text_size[1]
        org = (text_x, text_y)

        # Draw the text with a background for better visibility
        frame = cv2.rectangle(frame, (text_x - border, text_y_start - border), 
                              (text_x + text_size[0] + border, text_y + border), 
                              black_color, -1)
        frame = cv2.putText(frame, line, org, font, font_scale, white_color, thickness, cv2.LINE_AA)

        # Move to the next line
        text_y_start += text_size[1] + line_spacing




def caption(video, output_video, text, narration_time):
    input_video = video
    cap = cv2.VideoCapture(input_video)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
    
        ret, frame = cap.read()
        if not ret:
            break
        write_text("this is a sample text", frame)
        out.write(frame)


    cap.release()
    out.release()


input_video = '/Users/tylerklimas/Desktop/openaisandbox/videoCreation/cooking_with_audio_plus.mp4'
cap = cv2.VideoCapture(input_video)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = 'withtranscript.avi'
out = cv2.VideoWriter(output_video, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
