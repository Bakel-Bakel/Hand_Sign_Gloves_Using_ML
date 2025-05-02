import os
import socket
import time

HOST = ''
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print(f"Connected by {addr}")

buffer = ""

# Set your thresholds based on new calibration
thumb_bent_threshold = 120  # Thumb is bent if greater than 120
pinky_bent_threshold = 600  # Pinky is bent if greater than 600
pointer_bent_threshold = 139  # Pointer is bent if greater than 139
fourth_finger_bent_threshold = 134  # Fourth finger bent above 134

def say(text):
    print(f"Speaking: {text}")
    os.system(f'pico2wave -w temp.wav "{text}" && aplay temp.wav')

while True:
    data = conn.recv(4096)
    if not data:
        break

    decoded_data = data.decode()
    buffer += decoded_data

    lines = buffer.split('\n')
    buffer = lines[-1]

    if len(lines) > 1:
        latest_line = lines[-2].strip()

        if latest_line:
            values = latest_line.split(',')
            try:
                if len(values) >= 5:  # Assuming 5 values for fingers
                    # Extracting the finger values (Thumb, Pointer, Fourth, Pinky)
                    thumb_val = int(values[4])  # Thumb is the 5th element (index 4)
                    pointer_val = int(values[3])  # Pointer is the 4th element (index 3)
                    fourth_finger_val = int(values[1])  # Fourth finger (index 1)
                    pinky_val = int(values[0])  # Pinky is the 1st element (index 0)

                    current_time = time.time()

                    # Check if thumb is bent
                    if thumb_val > thumb_bent_threshold:
                        print("Thumb is bent")
                        say("Hi")  # Say "Hi" when the thumb is bent

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
