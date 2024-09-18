import socket
import json

# Define server settings
HOST = '127.0.0.1'
PORT = 65432

# Define Blender connection settings
BLENDER_HOST = 'localhost'
BLENDER_PORT = 65433

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(10)
        print("Server listening on", HOST, PORT)
        
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
                        send_to_blender(landmarks)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                except ValueError as e:
                    print(f"ValueError: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

def send_to_blender(landmarks):
    # Create a socket connection to Blender
    blender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    blender_socket.connect((BLENDER_HOST, BLENDER_PORT))

    # Send landmarks to Blender
    data = json.dumps(landmarks)
    data_length = str(len(data)) + '\n'
    blender_socket.sendall(data_length.encode('utf-8'))
    blender_socket.sendall(data.encode('utf-8'))

    # Close the socket connection
    blender_socket.close()

if __name__ == "__main__":
    start_server()
