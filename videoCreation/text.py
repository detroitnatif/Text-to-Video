import cv2


def write_text(text, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    thickness = 2  # Reduced thickness for better fit
    initial_font_scale = 1  # Start with a default font scale
    border = 5

    # Start with an initial font scale and decrease until the text fits the frame
    font_scale = initial_font_scale
    text_width = 0
    text_height = 0
    max_width = frame.shape[1]
    max_height = frame.shape[0]
    while True:
        # Calculate the size of the text at the current font scale
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_width, text_height = text_size
        # Break the loop if the text fits within the frame dimensions or if font scale is too small
        if text_width <= max_width and text_height <= max_height or font_scale <= 0.1:
            break
        # Decrease the font scale to try a smaller size
        font_scale -= 0.1

    text_x = (max_width - text_width) // 2
    text_y = (max_height + text_height) // 2  # Adjusted for vertical centering
    org = (text_x, text_y)

    # Draw the background for the text (optional, for better visibility)
    frame = cv2.rectangle(frame, (text_x - border, text_y - text_height - border), 
                          (text_x + text_width + border, text_y + border), 
                          black_color, -1)

    # Draw the text with a border (optional)
    frame = cv2.putText(frame, text, org, font, font_scale, black_color, thickness + border, cv2.LINE_AA)
    
    # Finally, draw the text
    frame = cv2.putText(frame, text, org, font, font_scale, white_color, thickness, cv2.LINE_AA)





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
