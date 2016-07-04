import socket

# HOST = socket.gethostbyname('raspberrypi')
HOST = input("Host: ")
PORT = 5000


def send_to_server(info):
    try:
        s.send(info.encode())
    except Exception as e:
        print(e)


def controls():
    print("8 | Forward")
    print("2 | Reverse")
    print("0 | Stop")
    print("4 | Turn Left")
    print("6 | Turn Right")
    print("5 | Centre Steering")

print("Attempting to connect to the server")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    print("Successfully connected to the server")
    controls()
except Exception as e:
    print(e)

while True:
    data = input("Enter a direction: ")
    send_to_server(data)
    reply = s.recv(1024)
    print(reply.decode())

