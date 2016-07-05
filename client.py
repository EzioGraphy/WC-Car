import socket
from time import sleep


HOST = input("Host : ")
PORT = 9000
POPUP = input("Would you like the webcam stream as a popup? y/n ")

# decide whether or not to use the popup and create it if desired
if POPUP == 'y':
    import numpy as np
    import cv2

    cap = cv2.VideoCapture('http://' + HOST + ':8081')
    while True:
        ret, frame = cap.read()
        cv2.imshow('WC Car - FPV', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cap.destroyAllWindows()

elif POPUP == 'n':
    print("If you would like to view the webcam stream please enter this ip in the url bar of your browser. ", HOST)
else:
    print("Invalid input.")
    pass


def send_to_server(info):
    try: s.send(info.encode())
    except Exception as e: print(e)


def commands():
    print("\n### Available Commands ###\n")
    print("++ MOVEMENT ++")
    print("8  | Forward")
    print("2  | Reverse")
    print("0  | Stop")
    print("4  | Turn Left")
    print("6  | Turn Right")
    print("5  | Centre Steering")
    print("\n++ Lighting ++")
    print("wh | Toggle white headlights")
    print("bh | Toggle blue headlights")
    print("bl | Toggle break lights")
    print("rl | Toggle reverse lights\n\n")


def debug_info():
    print("###################### DEBUG INFO #######################\n")
    print("flashing blue head lights means everything is ready to go")
    print("2 flashes with a gap of 0.5 seconds means command was not valid")
    print("5 flashes with a gap of 1 seconds means server cant communicate with client")
    print("2 flashes with a gap of 0.1 seconds means command was received")
    print("1 flash   with a gap of 1 seconds means the command was valid")
    print("5 flashes with a gap of 0.1 seconds means the server is ready\n\n")

print("\nAttempting to connect to the server...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checking if socket is able to be connected to
try:
    s.connect((HOST, PORT))
    print("Successfully connected to the server\n\n")
    s.close()
except Exception as e:
    print(e)

sleep(1)
commands()
sleep(3)
debug_info()

# MAIN
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: s.connect((HOST, PORT))
    except Exception as e: print(e)

    data = input("Enter a direction: ")
    send_to_server(data)
    reply = s.recv(1024)
    print(reply.decode())

