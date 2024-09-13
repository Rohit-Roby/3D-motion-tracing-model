import bpy
import socket
import json
import threading

# Define server settings
HOST = 'localhost'
PORT = 65432

# Set up the avatar rig (assuming you have an avatar rig)
def apply_landmarks_to_rig(landmarks):
    for i, landmark in enumerate(landmarks):
        # Map landmarks to avatar bones (you need to define this mapping)
        bone_name = f'Bone_{i}'
        if bone_name in bpy.context.object.pose.bones:
            bone = bpy.context.object.pose.bones[bone_name]
            bone.location = (landmark['x'], landmark['y'], landmark['z'])
            bone.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Blender server listening on", HOST, PORT)
        
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                landmarks = json.loads(data.decode('utf-8'))
                apply_landmarks_to_rig(landmarks)

# Run the server in a separate thread
def start_server_thread():
    threading.Thread(target=receive_data).start()

# Start the server
start_server_thread()
