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
last_W_time = 0
last_e_time = 0
last_are_time = 0
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
                    second_val = int(values[1])
                    middle_val = int(values[2])
                    pointer_val = int(values[3])
                    thumb_val = int(values[4])

                    current_time = time.time()

                    # Check for "H"
                    if thumb_val > 99 and pointer_val > 117:
                        #print("Detected H (Thumb and Pointer released)")
                        #say("H")
                        last_H_time = current_time

                    # Check for "I"
                    if (thumb_val < 97) and (pointer_val < 114) and (middle_val < 970) and (second_val < 120) and (pinky_val > 570):
                        #print("Detected I (All except Pinky bent)")
                        #say("I")
                        last_I_time = current_time

                    # Check for "Hi" (H + I within 5 seconds)
                    if abs(last_H_time - last_I_time) <= 5 and last_H_time != 0 and last_I_time != 0:
                        print("Detected Hi!")
                        say("Hi")
                        last_H_time = 0
                        last_I_time = 0

                    # Check for "W" (First and Fifth fingers bent, rest straight)
                    if thumb_val < 97 and second_val > 120 and middle_val > 970 and pointer_val > 117 and pinky_val < 570:
                        print("Detected W (First and Fifth bent, rest straight)")
                        say("W")
                        last_W_time = current_time

                    # Check for "e" (All fingers bent)
                    if thumb_val < 97 and pointer_val < 114 and middle_val < 970 and second_val < 120 and pinky_val < 570:
                        print("Detected e (All fingers bent)")
                        say("e")
                        last_e_time = current_time

                    # Check for "we" (W + e within 3 seconds)
                    if abs(last_W_time - last_e_time) <= 3 and last_W_time != 0 and last_e_time != 0:
                        print("Detected we!")
                        say("we")
                        last_W_time = 0
                        last_e_time = 0

                    # Check for "are" (All except first finger bent, wait for 3 seconds)
                    if thumb_val > 99 and pointer_val < 114 and middle_val < 970 and second_val < 120 and pinky_val < 570:
                        if current_time - last_are_time >= 3:
                            print("Detected are!")
                            say("are")
                            last_are_time = current_time

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
