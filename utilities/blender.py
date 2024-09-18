import bpy
import socket
import json
import threading

# Define server settings
HOST = 'localhost'
PORT = 65433

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Blender server listening on", HOST, PORT)

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                try:
                    # Read the length of the incoming data
                    length_data = b""
                    while b'\n' not in length_data:
                        length_data += conn.recv(1024)

                    length_str = length_data.decode('utf-8').strip()
                    data_length = int(length_str)

                    # Read the actual data
                    data = b""
                    while len(data) < data_length:
                        packet = conn.recv(1024)
                        if not packet:
                            print("Connection lost")
                            break
                        data += packet

                    try:
                        landmarks = json.loads(data.decode('utf-8'))
                        print("Received landmarks:", landmarks)

                        # Apply landmarks to avatar rig
                        apply_landmarks_to_rig(landmarks)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                except ValueError as e:
                    print(f"ValueError: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

def apply_landmarks_to_rig(landmarks):
    # Apply landmarks to avatar rig (assuming you have an avatar rig)
    for i, landmark in enumerate(landmarks):
        bone_name = f'Bone_{i}'
        if bone_name in bpy.context.object.pose.bones:
            bone = bpy.context.object.pose.bones[bone_name]
            bone.location = (landmark['x'], landmark['y'], landmark['z'])
            bone.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)

def start_server_thread():
    threading.Thread(target=receive_data).start()

# Start the server
start_server_thread()