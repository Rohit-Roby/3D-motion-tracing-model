# STEP 1: Import the necessary modules.
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

# STEP 2: Create an PoseLandmarker object.
model_path = 'pose_landmarker_heavy.task'
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the live stream mode:
# def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#     print('pose landmarker result: {}'.format(result))

def process_result(frame, landmarks: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    # ann_frame = draw_landmarks_on_image(frame, landmarks)
    return frame
    # cv2.imshow('frame', ann_frame)
    # if cv2.waitKey(1) == ord('q'):
    #     return
    
def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=process_result)

with PoseLandmarker.create_from_options(options) as landmarker:
  # The landmarker is initialized. Use it here.
  # ...
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cannot open camera")
        exit()
    while True:
        #capture Frame by frame
        ret, frame = cap.read()
        #if frame is read correctly ret is True
        if not ret:
            print("can't receive frame (stream end?). Exiting ...")
            break
        
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Run the PoseLandmarker on the image.
        landmarks = landmarker.detect_async(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
        # print(ann_img)
        ann_frame = draw_landmarks_on_image(frame, landmarks)
        cv2.imshow('frame', ann_frame)
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    # cv2.imshow('frame', annotated_image)
    
