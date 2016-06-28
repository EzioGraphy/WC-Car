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
a.digitalWrite(REAR_DIR_1, a.LOW);
a.digitalWrite(REAR_DIR_2, a.HIGH);
a.analogWrite(PWM_REAR, 200);
```
## Motivation

This project is being used as my year 12 major IPT project, and I thought it would be an interesting concept to explore. 

## Installation

Several Python packages are required such as ........

## License

A short snippet describing the license (MIT, Apache, etc.)
