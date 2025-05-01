import socket

HOST = ''  # Listen on all available interfaces
PORT = 1234  # Same port as ESP32

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received:", data.decode().strip())

conn.close()
