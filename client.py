import socket

HOST = input("Host: ")
PORT = 5000


def move(direction):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.send(direction.encode())
        s.close()
    except:
        print("Failed to establish a connection with the server.")

while True:
    data = input("Enter a direction: ")
    move(data)

