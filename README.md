# WiFi Controlled Car

## Synopsis

The WC-Car is built from an existing RC Car but has been heavily modified. The original control board (reciever, motor control etc.) was removed and replaced with a Raspberry Pi 3, Arduino Uno and a H bridge. The Raspberry Pi recives input from the client via a tcp connection which feeds commands to the Arduino through serial to execute. The Raspberry Pi is also hosting a webcam server. (A Genuino 101 was going to be used, but nampy firmware is not compatible with the x86 architecture.)


## Code Examples

### Motor Control
DC motors can either go forward or reverse depending on the polarity of the circuit, a H bridge is used to change the polarity and PWM is used to control the speed. The H bridge that was used is a l298n clone. The two input directions are toggled and a PWM signal is sent to the H bridge. Below is an example of the rear motor, the front motor which handles the steering is the exact same.

#### Arduino (C)
```c
digitalWrite(REAR_DIR_1, LOW);
digitalWrite(REAR_DIR_2, HIGH);
analogWrite(PWM_REAR, 200);
```

#### Python using the nampy package
```python

from nanpy import ArduinoApi, SerialManager

connection = SerialManager()
a = ArduinoApi(connection=connection)

a.digitalWrite(REAR_DIR_1, a.LOW);
a.digitalWrite(REAR_DIR_2, a.HIGH);
a.analogWrite(PWM_REAR, 200);
```
## Motivation

This project is being used as my year 12 major IPT project, and I thought it would be an interesting concept to explore. 

## Installation

#### Arduino
The Arduino must be using theh nanpy firmware which will be linked below

#### Raspberry Pi
The Motion package must be installed which can retrieved through apt-get to host a webcam server. Apache is optional but it can be used to make a nicer looking website with the webcam stream embedded.

The Raspberry Pi must have Python3 installed as the server is written is Python3.5

#### Client
Python3 for the same reason above
The OpenCV2 python3 library if you would prefer the webcam stream to be in a window instead of a browser

### Links
https://nanpy.github.io

http://opencv.org

## License

The MIT License (MIT)

Copyright (c) 2016 Lochie Ashcroft

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
