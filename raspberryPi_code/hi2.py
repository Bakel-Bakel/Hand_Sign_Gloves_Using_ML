import socket
import time
import pyttsx3

# Setup TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speaking

HOST = ''   # Listen on all interfaces
PORT = 1234 # Must match ESP32

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print(f"Connected by {addr}")

buffer = ""
last_H_time = 0
last_I_time = 0

def say(text):
    engine.say(text)
    engine.runAndWait()

while True:
    data = conn.recv(4096)
    if not data:
        break

    decoded_data = data.decode()
    buffer += decoded_data

    lines = buffer.split('\n')
    buffer = lines[-1]  # Keep incomplete line

    if len(lines) > 1:
        latest_line = lines[-2].strip()

        if latest_line:
            values = latest_line.split(',')
            try:
                if len(values) >= 8:  # 5 flex + 3 imu = 8 elements
                    # Extract important finger values
                    pinky_val = int(values[0])
                    pointer_val = int(values[3])
                    thumb_val = int(values[4])

                    current_time = time.time()

                    # Check for H
                    if thumb_val > 99 and pointer_val > 117:
                        print("Detected H (Thumb and Pointer released)")
                        engine.stop()
                        # Small wait to make sure speaker is ready
                        time.sleep(0.5)
                        say("H")
                        last_H_time = current_time

                    # Check for I
                    if (thumb_val < 97) and (pointer_val < 114) and (pinky_val > 570):
                        print("Detected I (Only Pinky Released)")
                        say("I")
                        last_I_time = current_time

                    # Check for Hi (within 3 seconds interval)
                    if abs(last_H_time - last_I_time) <= 3 and last_H_time != 0 and last_I_time != 0:
                        print("Detected Hi!")
                        say("Hi")
                        # Reset to prevent multiple Hi announcements
                        last_H_time = 0
                        last_I_time = 0

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
