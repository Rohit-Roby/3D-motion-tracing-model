import mediapipe as mp
import numpy as np
import cv2 

# Use OpenCV’s VideoCapture to start capturing from the webcam.
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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) == ord('q'):
        break
    # cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows
# Create a loop to read the latest frame from the camera using VideoCapture#read()

# Convert the frame received from OpenCV to a MediaPipe’s Image object.
# mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)
    