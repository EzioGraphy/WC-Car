## WiFi Controlled Car

## Synopsis

The WC-Car is built from an existing RC Car but has been heavily modified. The original control board (reciever, motor control etc.) was removed and replaced with an Arduino 101 and a H bridge to control the motors. The Arduino has full controll of the motors and the Raspberry Pi recieves input from the user which is then sent to the Arduino 101 and it also hosts a webcam server.

## Code Example

Motor Control
DC motors can either go forward or reverse depending on the polarity of the circuit, a H bridge is used to change the polarity and PWM is used to control the speed. The H bridge that was used is a l298n clone. The two input directions are toggled and a PWM signal is sent to the H bridge. Below is an example of the rear motor, the front motor which handles the steering is the exact same.

digitalWrite(Rear_Dir_1, LOW);
digitalWrite(Rear_Dir_2, HIGH);
analogWrite(PWM_Rear, 200);

## Motivation

This project is being used as my year 12 major IPT project, and I thought it would be an interesting concept to explore. 

## Installation

Several Python packages are required such as ........

## License

A short snippet describing the license (MIT, Apache, etc.)
