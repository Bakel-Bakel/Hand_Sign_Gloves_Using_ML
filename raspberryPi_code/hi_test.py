import os
import socket
import time
import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# OLED setup (128x64)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# Create image buffer
image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)

# Load the default font
font = ImageFont.load_default()


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

                        # Draw the text "Hello" at the top-left corner
                        draw.text((0, 0), "hi, We are BME of 25", font=font, fill=255)

                        # Display the image with the drawn text
                        oled.image(image)
                        oled.show()

                        # Keep the "Hello" message visible for 5 seconds
                        time.sleep(5)

                        # Clear the display after the delay
                        oled.fill(0)
                        oled.show()
                        time.sleep(5)
                        '''say("we")
                        time.sleep(6)
                        say("are")
                        time.sleep(6)
                        say("B")
                        time.sleep(1)
                        say("M")
                        time.sleep(1)
                        say("E")
                        time.sleep(4)
                        say("of")
                        time.sleep(5)
                        say("25")'''
                       
                    
                    '''# First signal (for "t"): All fingers bent
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
                    if abs(last_signal_time_w - last_signal_time_e) <= 7 and last_signal_time_w != 0 and last_signal_time_e != 0:
                        print("Detected 'we'!")
                        say("we")
                        last_signal_time_w = 0
                        last_signal_time_e = 0
                        time.sleep(6)
                        say("are")
                        time.sleep(6)
                        say("B")
                        time.sleep(1)
                        say("M")
                        time.sleep(1)
                        say("E")
                        time.sleep(4)
                        say("of")
                        time.sleep(5)
                        say("25")

            except Exception as e:
                print(f"Error processing data: {e}")

conn.close()
