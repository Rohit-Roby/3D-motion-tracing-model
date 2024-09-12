# STEP 1: Import the necessary modules.
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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

def draw_landmarks_on_livestream(image, ann_img):
    if ann_img is None:
        return image    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    mp_drawing_style = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
    mp_drawing.draw_landmarks(image, ann_img.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing_style)
    # cv2.imshow('frame', image)
    return image

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,result_callback=draw_landmarks_on_livestream)

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
        #our preperation on the frame come here
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarks = landmarker.detect_async(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
        # print(ann_img)
        ann_frame = draw_landmarks_on_livestream(frame, landmarks)
        cv2.imshow('frame', ann_frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # cv2.imshow('frame', annotated_image)
    
