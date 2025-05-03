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
last_signal_time_1 = 0  # Time when the first signal was detected
last_signal_time_2 = 0  # Time when the second signal was detected
last_spoken_time = 0
last_signal_time_w = 0
last_signal_time_e = 0
last_signal_time_a = 0
last_signal_time_are = 0
last_signal_time_B = 0  # Time when the first signal (B) was detected
last_signal_time_M = 0  # Time when the second signal (M) was detected
last_spoken_time = 0


# Set calibration thresholds
thumb_straight_threshold = 120  # Thumb straight if below 120
thumb_bent_threshold = 120     # Thumb bent if above 120
pointer_straight_mean = 135  # Pointer straight mean around 135
pointer_bent_threshold = 139  # Pointer bent if greater than 139
fourth_bent_threshold = 134  # Fourth finger bent if above 134
pinky_bent_threshold = 600  # Pinky bent if above 600

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
                    thumb_val = int(values[4])  # Thumb is the 5th element (index 4)
                    pointer_val = int(values[3])  # Pointer is the 4th element (index 3)
                    fourth_finger_val = int(values[1])  # Fourth finger (index 1)
                    pinky_val = int(values[0])  # Pinky is the 1st element (index 0)
                    middle_finger_val = int(values[2])  # Middle finger (index 2)

                    current_time = time.time()

                    # First signal: Thumb and pointer straight, rest bent
                    if  pointer_val < 138 and pointer_val > 117 \
                        and fourth_finger_val > 134 and pinky_val > pinky_bent_threshold:
                        print("First signal detected: Thumb and pointer straight, rest bent.")
                        last_signal_time_1 = current_time

                    # Second signal: Pinky straight, rest bent
                    if pinky_val < pinky_bent_threshold and thumb_val > thumb_bent_threshold and pointer_val > pointer_bent_threshold \
                         and fourth_finger_val > 134:
                        print("Second signal detected: Pinky straight, rest bent.")
                        last_signal_time_2 = current_time

                    # Check if both signals happened within 5 seconds
                    if abs(last_signal_time_1 - last_signal_time_2) <= 10 and last_signal_time_1 != 0 and last_signal_time_2 != 0:
                        print("Detected Hi!")
                        say("Hi")
                        last_signal_time_1 = 0
                        last_signal_time_2 = 0
                    '''
                    # First signal (for "t"): All fingers bent
                    if thumb_val > thumb_bent_threshold and pointer_val > pointer_bent_threshold \
                         and fourth_finger_val > 134 and pinky_val > pinky_bent_threshold:
                        print("First signal detected: All fingers bent.")
                        last_signal_time_t = current_time

                    # Second signal (for "h"): Thumb and pointer straight, rest bent
                    if  pointer_val < 138 and pointer_val > 117 \
                        and fourth_finger_val > 134 and pinky_val > pinky_bent_threshold:
                        print("First signal detected: Thumb and pointer straight, rest bent.")
                        last_signal_time_h = current_time

                    # Check if both "t" and "h" signals are met
                    if abs(last_signal_time_t - last_signal_time_h) <= 5 and last_signal_time_t != 0 and last_signal_time_h != 0:
                        time.sleep(2)
                        print("Detected 'the'!")
                        say("the")
                        last_signal_time_t = 0
                        last_signal_time_h = 0'''
                    # First signal (for "w"): First, second, and fourth fingers straight, fifth bent
                    if thumb_val < thumb_straight_threshold and pointer_val < 138 \
                        and fourth_finger_val < fourth_bent_threshold and pinky_val > pinky_bent_threshold:
                        print("First signal detected: First, second, and fourth fingers straight, fifth bent (W).")
                        last_signal_time_w = current_time

                    # Second signal (for "e"): All fingers bent
                    if thumb_val > thumb_bent_threshold and pointer_val > pointer_bent_threshold and \
                        fourth_finger_val > fourth_bent_threshold and pinky_val > pinky_bent_threshold:
                        print("Second signal detected: All fingers bent (E).")
                        last_signal_time_e = current_time

                    # Check if both "w" and "e" signals are met within 3 seconds
                    if abs(last_signal_time_w - last_signal_time_e) <= 3 and last_signal_time_w != 0 and last_signal_time_e != 0:
                        print("Detected 'we'!")
                        say("we")
                        last_signal_time_w = 0
                        last_signal_time_e = 0

                    if thumb_val > thumb_bent_threshold and pointer_val > pointer_bent_threshold  \
                        and fourth_finger_val > fourth_bent_threshold and pinky_val < pinky_bent_threshold:
                        print("First signal detected: All fingers bent, pinky straight (A).")
                        last_signal_time_a = current_time

                    # Second signal (for "are"): Thumb and pointer straight, rest bent
                    if thumb_val < thumb_straight_threshold and pointer_val < 138 \
                         and fourth_finger_val > 134 and pinky_val > pinky_bent_threshold:
                        print("Second signal detected: Thumb and pointer straight, rest bent (ARE).")
                        say("are")
                        last_signal_time_are = current_time

                    # Check if both "a" and "are" signals are met within 5 seconds
                    if abs(last_signal_time_a - last_signal_time_are) <= 7 and last_signal_time_a != 0 and last_signal_time_are != 0:
                        print("Detected 'are'!")
                        say("are")
                        last_signal_time_a = 0
                        last_signal_time_are = 0
                    
                    if thumb_val > thumb_bent_threshold and pointer_val < 138 \
                         and fourth_finger_val < 134 and pinky_val < pinky_bent_threshold:
                        print("First signal detected: All fingers straight except thumb bent (B).")
                        last_signal_time_B = current_time
                        # Second signal (for "M"): All fingers bent
                        if thumb_val > thumb_bent_threshold and pointer_val > pointer_bent_threshold  \
                            and fourth_finger_val > fourth_bent_threshold and pinky_val > pinky_bent_threshold:
                            print("Second signal detected: All fingers bent (M).")
                            last_signal_time_M = current_time

                        # Check if both "B" and "M" signals are met within 3 seconds
                        if abs(last_signal_time_B - last_signal_time_M) <= 5 and last_signal_time_B != 0 and last_signal_time_M != 0:
                            time.sleep(1.5)
                            print("Detected 'E'!")
                            say("E")
                            last_signal_time_B = 0
                            last_signal_time_M = 0

                            time.sleep(3)
                            say("of")

                            time.sleep(4)
                            say("25")

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
