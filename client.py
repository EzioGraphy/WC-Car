import socket

HOST = input("Host : ")
PORT = 9000


def send_to_server(info):
    try: s.send(info.encode())
    except Exception as e: print(e)

def controls():
    print(" CONTROLS ")
    print("8  | Forward")
    print("2  | Reverse")
    print("0  | Stop")
    print("4  | Turn Left")
    print("6  | Turn Right")
    print("5  | Centre Steering")
    print("\n")
    
print("Attempting to connect to the server...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checking if socket is able to be connected to
try:
    s.connect((HOST, PORT))
    print("Successfully connected to the server\n\n")
    s.close()
except Exception as e:
    print(e)

controls()
# MAIN
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: s.connect((HOST, PORT))
    except Exception as e: print(e)
    data = input("Enter a direction: ")
    send_to_server(data)
    reply = s.recv(1024)
    print(reply.decode())

