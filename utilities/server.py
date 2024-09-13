import socket
import json

# Define server settings
HOST = '127.0.0.1'
PORT = 65432

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
    # For demonstration, we just print landmarks
    # Replace this with actual code to send data to Blender
    print("Sending data to Blender:", landmarks)

if __name__ == "__main__":
    start_server()
