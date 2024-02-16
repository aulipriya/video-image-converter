import cv2
import numpy as np
import os
import mediapipe as mp
from deepface import DeepFace


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
            rois = detect_faces(frame)
            if rois:
                person_recognized = 0
                for roi in rois:
                    if recognize_face(roi):
                        person_recognized += 1
                print(f"Person Recognized {person_recognized}")
                if person_recognized > 0:
                    cv2.imwrite(f'../output_images/{count}.jpg', frame)
            count += int(fps)  # i.e. at 30 fps, this advances one second
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            ret, frame = cap.read()
            print(count)
        else:
            # release the video capture object
            cap.release()


def detect_faces(image):
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    face_detection_results = face_detection.process(image[:, :, ::-1])
    roi_s = []
    if face_detection_results.detections:
        for face in face_detection_results.detections:
            face_react = np.multiply(
                [
                    face.location_data.relative_bounding_box.xmin,
                    face.location_data.relative_bounding_box.ymin,
                    face.location_data.relative_bounding_box.width,
                    face.location_data.relative_bounding_box.height,
                ],
                [image.shape[1], image.shape[0], image.shape[1], image.shape[0]],
            ).astype(int)
            roi = image[face_react[1]:face_react[1]+face_react[3], face_react[0]:face_react[0]+face_react[2]]
            roi_s.append(roi)
        return roi_s

    else:
        return False


def recognize_face(face):
    try:
        dfs = DeepFace.find(img_path=face, db_path="../database/")
        if dfs[0].shape[0] > 0 and dfs[0]['VGG-Face_cosine'].loc[0] < 0.4:
            return dfs[0]['identity'].loc[0].split('/')[2]
        else:
            return False
    except ValueError:
        return False


if __name__ == "__main__":
    for video_file in os.listdir("../"):
        if video_file.endswith('.mkv') or video_file.endswith('.mp4'):
            create_images_from_video_file('../' + video_file)



