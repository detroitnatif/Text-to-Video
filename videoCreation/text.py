import cv2


def write_text(text, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0,0,0)
    thickness = 10
    font_scale = 3
    border = 5

    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = ((frame.shape[1]  -  text_size[0] ) // 2)
    text_y = (frame.shape[0]  // 2)
    org = (text_x, text_y)

    frame = cv2.putText(frame, text, org, font, font_scale, black_color, thickness + border * 2, cv2.LINE_AA)
    frame = cv2.putText(frame, text, org, font, font_scale, white_color, thickness , cv2.LINE_AA)





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
