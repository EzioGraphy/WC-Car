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
# MOTORS
PWM_REAR = 9
REAR_DIR_1 = 10
REAR_DIR_2 = 11

PWM_FRONT = 3
FRONT_DIR_1 = 2
FRONT_DIR_2 = 4

# LIGHTING
DEBUG = 5
WHITE_HEAD = 6
BLUE_HEAD = 7
BREAK = 8
REVERSE = 12

# Boolean
WHITE_HEAD_STATUS = False
BLUE_HEAD_STATUS = False
BREAK_STATUS = False
REVERSE_STATUS = False

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

a.pinMode(DEBUG, a.OUTPUT)
a.pinMode(WHITE_HEAD, a.OUTPUT)
a.pinMode(BLUE_HEAD, a.OUTPUT)
a.pinMode(BREAK, a.OUTPUT)
a.pinMode(REVERSE, a.OUTPUT)
print("Finished setting up PinModes")

################
#
#   SERVER
#
##################

HOST = ''
PORT = 9000
BUFFER_SIZE = 20


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
        debug(5, 1)

    a.analogWrite(PWM_FRONT, 0)
    # springs pull wheels back to centre


def stop():
    toggle_break()
    print("stopping")
    try:
        conn.send("Moving forward...".encode())
    except:
        reset_steering()
        stop()
        debug(5, 1)
        
    a.analogWrite(PWM_FRONT, 0)
    a.analogWrite(PWM_REAR, 0)

    sleep(1)
    toggle_break()


def forward():
    print("forward")

    # car will stop if it has lost connection with client
    try:
        conn.send("Moving forward...".encode())
    except:
        reset_steering()
        stop()
        debug(5, 1)

    a.digitalWrite(REAR_DIR_1, a.HIGH)
    a.digitalWrite(REAR_DIR_2, a.LOW)
    a.analogWrite(PWM_REAR, 255)
    sleep(2)
    a.analogWrite(PWM_REAR, 0)
    sleep(1)

    
def reverse():
    toggle_reverse()
    print("reversing")

    # car will stop if it has lost connection with client
    try:
        conn.send("Reversing...".encode())
    except:
        reset_steering()
        stop()
        debug(5, 1)

    a.digitalWrite(REAR_DIR_1, a.LOW)
    a.digitalWrite(REAR_DIR_2, a.HIGH)
    a.analogWrite(PWM_REAR, 255)  # full speed
    sleep(2)
    a.analogWrite(PWM_REAR, 0)  # so the car doesnt drive off if connection is lost
    sleep(1)
    toggle_reverse()
    

def turn_left():
    print("turning left")
    # car will stop if it has lost connection with client
    try:
        conn.send("Turning Left...".encode())
    except:
        reset_steering()
        stop()
        debug(5, 1)

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
        debug(5, 1)

    a.digitalWrite(FRONT_DIR_1, a.LOW)
    a.digitalWrite(FRONT_DIR_2, a.HIGH)
    a.analogWrite(PWM_FRONT, 255)
    # locks steering

# HEADLIGHTS


def toggle_white_head():
    global WHITE_HEAD_STATUS
    WHITE_HEAD_STATUS = not WHITE_HEAD_STATUS
    a.digitalWrite(WHITE_HEAD, WHITE_HEAD_STATUS)


def toggle_blue_head():
    global BLUE_HEAD_STATUS
    BLUE_HEAD_STATUS = not BLUE_HEAD_STATUS
    a.digitalWrite(BLUE_HEAD, BLUE_HEAD_STATUS)


def toggle_break():
    global BREAK_STATUS
    BREAK_STATUS = not BREAK_STATUS
    a.digitalWrite(BREAK, BREAK_STATUS)


def toggle_reverse():
    global REVERSE_STATUS
    REVERSE_STATUS = not REVERSE_STATUS
    a.digitalWrite(REVERSE, REVERSE_STATUS)


def debug(n, t):  # number of times to flash and time between flashes
    global DEBUG_STATUS
    for x in range(0, n):
        DEBUG_STATUS = not DEBUG_STATUS
        a.digitalWrite(DEBUG, DEBUG_STATUS)
        sleep(t)
    a.digitalWrite(DEBUG, a.LOW)  # Makes sure debug light never stays on

# user input to direction
commands = {
    # movement
    '8': forward,
    '2': reverse,
    '4': turn_left,
    '6': turn_right,
    '5': reset_steering,
    '0': stop,
    # lighting
    'wh': toggle_white_head,
    'bh': toggle_blue_head,
    'bl': toggle_break,
    'rl': toggle_reverse
}

################
#              #
#     Main     #
#              #
################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("Server is ready, awaiting a connection...")
debug(5, 0.1)

# flash blue headlights --> everything is ready
for x in range(0, 5):
    toggle_blue_head()
    sleep(0.25)

while True:
    s.listen(5)  # 5 connections because why not
    conn, addr = s.accept()
    print("Connection from ", addr)
    data = conn.recv(BUFFER_SIZE)
    debug(2, 0.1)
    # DEBUG LED 2 pulses
    try:
        print(data.decode())
        move = commands[data.decode()]
        move()
        debug(1, 1)
    except:
        print("Incorrect input")
        conn.send("Incorrect input".encode())
        debug(2, 0.5)

# DEBUG INFO

#  flashing blue head lights means everything is ready to go
#  2 flashes with a gap of 0.5 seconds means command was not valid
#  5 flashes with a gap of 1 seconds means server cant communicate with client
#  2 flashes with a gap of 0.1 seconds means command was received
#  1 flash   with a gap of 1 seconds means the command was valid
#  5 flashes with a gap of 0.1 seconds means the server is ready
