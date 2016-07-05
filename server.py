""" Input is sent via a tcp connection, input is checked against dictionary, movement in that direction occurs """
import socket
from time import sleep
from nanpy import ArduinoApi, SerialManager

###############
#             #
#   Arduino   #
#             #
###############

a = ''  # fixes issue with declaring a private variable in the try statement
PWM_REAR = 9
REAR_DIR_1 = 10
REAR_DIR_2 = 11

PWM_FRONT = 3
FRONT_DIR_1 = 2
FRONT_DIR_2 = 4

# DEBUG LED

# Connecting to Arduino via serial
print("Connecting to Arduino...")
try:
    connection = SerialManager()
    a = ArduinoApi(connection=connection)
    print("Successfully established a connection with the Arduino")
except:
    print("Failed to establish a connection with the Arduino")

# PinModes
print("Setting up PinModes on Arduino...")
a.pinMode(PWM_REAR, a.OUTPUT)
a.pinMode(REAR_DIR_1, a.OUTPUT)
a.pinMode(REAR_DIR_2, a.OUTPUT)

a.pinMode(PWM_FRONT, a.OUTPUT)
a.pinMode(FRONT_DIR_1, a.OUTPUT)
a.pinMode(FRONT_DIR_2, a.OUTPUT)
print("Finished setting up PinModes")

################
#              #
#   Movement   #
#              #
################

def reset_steering():
    print("resetting steering")
    try:
        conn.send("Moving forward...".encode())
    except:
        reset_steering()
        stop()
    a.analogWrite(PWM_FRONT, 0)
    # springs pull wheels back to centre


def stop():
    print("stopping")
    try:
        conn.send("Moving forward...".encode())
    except:
        reset_steering()
        stop()
        
    a.analogWrite(PWM_FRONT, 0)
    a.analogWrite(PWM_REAR, 0)


def forward():
    print("forward")

    # car will stop if it has lost connection with client
    try:
        conn.send("Moving forward...".encode())
    except:
        reset_steering()
        stop()

    a.digitalWrite(REAR_DIR_1, a.HIGH)
    a.digitalWrite(REAR_DIR_2, a.LOW)
    a.analogWrite(PWM_REAR, 255)
    sleep(2)
    a.analogWrite(PWM_REAR, 0)
    sleep(1)

    
def reverse():
    print("reversing")

    # car will stop if it has lost connection with client
    try:
        conn.send("Reversing...".encode())
    except:
        reset_steering()
        stop()

    a.digitalWrite(REAR_DIR_1, a.LOW)
    a.digitalWrite(REAR_DIR_2, a.HIGH)
    a.analogWrite(PWM_REAR, 255) # full speed
    sleep(2)
    a.analogWrite(PWM_REAR, 0)  # so the car doesnt drive off if connection is lost
    sleep(1)
    

def turn_left():
    print("turning left")
    # car will stop if it has lost connection with client
    try:
        conn.send("Turning Left...".encode())
    except:
        reset_steering()
        stop()

    a.digitalWrite(FRONT_DIR_1, a.HIGH)
    a.digitalWrite(FRONT_DIR_2, a.LOW)
    a.analogWrite(PWM_FRONT, 255)
    # locks steering


def turn_right():
    print("turning right")

    # car will stop if it has lost connection with client
    try:
        conn.send("Turning Right...".encode())
    except:
        reset_steering()
        stop()

    a.digitalWrite(FRONT_DIR_1, a.LOW)
    a.digitalWrite(FRONT_DIR_2, a.HIGH)
    a.analogWrite(PWM_FRONT, 255)
    # locks steering


# user input to direction
directions = {
    # numpad control
    '8': forward,
    '2': reverse,
    '4': turn_left,
    '6': turn_right,
    '5': reset_steering,
    '0': stop
    # other layout below
}

################
#              #
#     Main     #
#              #
################
HOST = ''
PORT = 9000
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("binded server")
print("awaiting connection...")

while True:
    s.listen(5)
    conn, addr = s.accept()
    print("Connection from ", addr)
    data = conn.recv(BUFFER_SIZE)
    # DEBUG LED 2 pulses
    try:
        print(data.decode())
        move = directions[data.decode()]
        move()
    except:
        print("Incorrect input")
        conn.send("Incorrect input".encode())
