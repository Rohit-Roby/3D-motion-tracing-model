# STEP 1: Import the necessary modules.
import cv2
import numpy as np
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()


while True:
  ret,frame = cap.read()
  flipped = cv2.flip(frame, flipCode=1)
  frame1 = cv2.resize(flipped,(640,640))
  rgb_img = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
  result = pose.process(rgb_img)
  print(result.pose_landmarks)

  mp_draw.draw_landmarks(frame1, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
  cv2.imshow("frame",frame1)
  
  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
    break

    
