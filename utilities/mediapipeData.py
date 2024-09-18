import socket
import json
import mediapipe as mp
import cv2

# Define server settings
HOST = '127.0.0.1'
PORT = 65432

cap = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# def send_landmarks_to_server(landmarks):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         print(s)
#         s.connect((HOST, PORT))
#         while True:
#             # msg = 'CLIENT >> '
#             # s.send(msg)
#             # msg = s.recv(1024)
#             # print('SERVER >> ', msg)
#         # Convert landmarks to JSON format
#             data = json.dumps(landmarks)
#             # length_str = f"{len(data)}\n"
#             # Send length of the data
#             # s.sendall(length_str.encode('utf-8'))
#             # Send the actual data
#             s.sendall(data.encode('utf-8'))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Process the frame
    flipped = cv2.flip(frame, flipCode=1)
    frame1 = cv2.resize(flipped,(640,640))
    rgb_img = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_img)
    mp_draw.draw_landmarks(frame1, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#   Display the frame (optional)
    
    # Extract landmarks
    if results.pose_landmarks:
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.append({
                'x': float(landmark.x),
                'y': float(landmark.y),
                'z': int(landmark.z)
            })
        # Send landmarks to the server
        # print(landmarks)
        # Send landmarks to server
        data = json.dumps(landmarks)
        data_length = str(len(data)) + '\n'
        s.sendall(data_length.encode('utf-8'))
        s.sendall(data.encode('utf-8'))
    
    cv2.imshow('MediaPipe Pose', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
pose.close()
cap.release()
cv2.destroyAllWindows()
