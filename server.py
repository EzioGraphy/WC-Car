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

# Connecting to Arduino via serial
print("Connecting to Arduino...")
try:
    connection = SerialManager()
    a = ArduinoApi(connection=connection)
    print("Successfully established a connection with the Arduino")
except:
    print("Failed to establish a connection with the Arduino")

# PinModes
a.pinMode(PWM_REAR, a.OUTPUT)
a.pinMode(REAR_DIR_1, a.OUTPUT)
a.pinMode(REAR_DIR_2, a.OUTPUT)

a.pinMode(PWM_FRONT, a.OUTPUT)
a.pinMode(FRONT_DIR_1, a.OUTPUT)
a.pinMode(FRONT_DIR_2, a.OUTPUT)


################
#              #
#   Movement   #
#              #
################

def forward():
    print("moving forward")
    a.digitalWrite(REAR_DIR_1, a.LOW)
    a.digitalWrite(REAR_DIR_2, a.HIGH)
    a.analogWrite(PWM_REAR, 200)
    sleep(2)
    a.analogWrite(PWM_REAR, 0)


def reverse():
    print("reversing")
    a.digitalWrite(REAR_DIR_1, a.HIGH)
    a.digitalWrite(REAR_DIR_2, a.LOW)
    a.analogWrite(PWM_REAR, 200)
    sleep(2)
    a.analogWrite(PWM_REAR, 0)


def left():
    print("turning left")
    a.digitalWrite(FRONT_DIR_1, a.HIGH)
    a.digitalWrite(FRONT_DIR_2, a.LOW)
    a.analogWrite(PWM_FRONT, 200)
    sleep(2)
    a.analogWrite(PWM_FRONT, 0)


def right():
    print("turning right")
    a.digitalWrite(FRONT_DIR_1, a.LOW)
    a.digitalWrite(FRONT_DIR_2, a.HIGH)
    a.analogWrite(PWM_FRONT, 200)
    sleep(2)
    a.analogWrite(PWM_FRONT, 0)


def halt():
    print("halting")
    a.analogWrite(PWM_FRONT, 0)
    a.analogWrite(PWM_REAR, 0)

# user input to direction
directions = {
    '8': forward,
    '2': reverse,
    '4': left,
    '6': right,
    '5': halt
}

################
#              #
#     Main     #
#              #
################

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5000))
    s.listen(1)
    conn, addr = s.accept()
    print("Connection from ", addr)
    data = conn.recv(64)
    try:
        move = directions[data.decode()]
        move()
    except:
        print("Incorrect input")
