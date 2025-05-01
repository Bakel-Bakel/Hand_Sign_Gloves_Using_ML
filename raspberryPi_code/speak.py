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

while True:
    data = conn.recv(4096)
    if not data:
        break

    decoded_data = data.decode()
    buffer += decoded_data

    lines = buffer.split('\n')
    buffer = lines[-1]  # Incomplete line

    if len(lines) > 1:
        latest_line = lines[-2].strip()

        if latest_line:
            values = latest_line.split(',')
            try:
                first_value = values[0]
                print(f"First flex value (latest line): {first_value}")

                # Speak the first value
                engine.say(f"{first_value}")
                engine.runAndWait()

                time.sleep(1)  # Short wait before next

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
