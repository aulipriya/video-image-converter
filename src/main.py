import cv2
import numpy as np
import os


def create_images_from_video_file(video_path):
    # Creating a VideoCapture object to read the video
    cap = cv2.VideoCapture(video_path, )
    ret, frame = cap.read()
    # Loop until the end of the video
    count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not os.path.exists("../output_images/"):
        os.makedirs("../output_images/")
    while cap.isOpened():
        # Capture frame-by-frame
        if ret:
            cv2.imwrite(f'../output_images/{count}.jpg', frame)
            count += int(fps)  # i.e. at 30 fps, this advances one second
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            ret, frame = cap.read()
            count += 1
            print(count)
        else:
            # release the video capture object
            cap.release()


if __name__ == "__main__":
    create_images_from_video_file("../dance_video_test.mp4")




