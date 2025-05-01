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
last_H_time = 0
last_I_time = 0
last_spoken_time = 0

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
                if len(values) >= 8:
                    pinky_val = int(values[0])
                    pointer_val = int(values[3])
                    thumb_val = int(values[4])

                    current_time = time.time()

                    if (current_time - last_spoken_time) >= 1.0:
                        if abs(last_H_time - last_I_time) <= 9 and last_H_time != 0 and last_I_time != 0:
                            print("Detected Hi!")
                            say("Hi")
                            last_H_time = 0
                            last_I_time = 0

                        elif thumb_val > 99 and pointer_val > 117:
                            print("Detected H (Thumb and Pointer released)")
                            say("H")
                            last_H_time = current_time

                        elif (thumb_val < 97) and (pointer_val < 114) and (pinky_val > 570):
                            print("Detected I (Only Pinky Released)")
                            say("I")
                            last_I_time = current_time

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
