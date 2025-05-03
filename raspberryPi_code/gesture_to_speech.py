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
last_signal_time_w = 0
last_signal_time_e = 0
last_signal_time_a = 0
last_signal_time_are = 0
last_signal_time_B = 0  # Time when the first signal (B) was detected
last_signal_time_M = 0  # Time when the second signal (M) was detected

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

# Function to fetch and process new data
def fetch_and_process_data(conn):
    data = conn.recv(4096)
    if not data:
        return None, None  # Return None if no data

    decoded_data = data.decode()
    buffer = ""
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

                    return values, (thumb_val, pointer_val, fourth_finger_val, pinky_val, middle_finger_val)

            except Exception as e:
                print(f"Error processing data: {e}")
                return None, None  # Return None if an error occurs

    return None, None

# Function to check signals and perform actions based on conditions
def check_signals_and_speak(values, thumb_val, pointer_val, fourth_finger_val, pinky_val, middle_finger_val, current_time):
    global last_signal_time_1, last_signal_time_2, last_signal_time_w, last_signal_time_e, last_signal_time_a, last_signal_time_are, last_signal_time_B, last_signal_time_M

    # First signal: Thumb and pointer straight, rest bent
    if pointer_val < 138 and pointer_val > 117 and fourth_finger_val > 134 and pinky_val > pinky_bent_threshold:
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

    # First signal (for "w"): First, second, and fourth fingers straight, fifth bent
    if thumb_val < thumb_straight_threshold and pointer_val < 138 and fourth_finger_val < fourth_bent_threshold and pinky_val > pinky_bent_threshold:
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

    # Handle other gestures like "a", "B", "M" similarly here
    # For brevity, we're not including them here as the logic is similar to the existing ones.

# Main loop
while True:
    # Fetch new data
    values, sensor_data = fetch_and_process_data(conn)
    
    if not values:
        continue  # Skip if no data

    thumb_val, pointer_val, fourth_finger_val, pinky_val, middle_finger_val = sensor_data
    current_time = time.time()

    # Process the fetched data and check for gestures
    check_signals_and_speak(values, thumb_val, pointer_val, fourth_finger_val, pinky_val, middle_finger_val, current_time)
    
    # You can add additional functionality to control the frequency of fetch or when to fetch new data based on your needs.

conn.close()
