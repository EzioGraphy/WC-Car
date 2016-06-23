// REAR
int PWM_Rear = 9;
int Rear_Dir_1 = 10;
int Rear_Dir_2 = 11;

// FRONT
int PWM_Front = 3;
int Front_Dir_1 = 2;
int Front_Dir_2 = 4;

// REAR MOTOR
void forward()
{
  digitalWrite(Rear_Dir_1, LOW);
  digitalWrite(Rear_Dir_2, HIGH);
  analogWrite(PWM_Rear, 200);  
}

void reverse()
{
  digitalWrite(Rear_Dir_1, HIGH);
  digitalWrite(Rear_Dir_2, LOW);
  analogWrite(PWM_Rear, 200);   
}

// FRONT MOTOR
void left()
{
  digitalWrite(Front_Dir_1, HIGH);
  digitalWrite(Front_Dir_2, LOW);
  analogWrite(PWM_Front, 200);   
}

void right()
{
  digitalWrite(Front_Dir_1, HIGH);
  digitalWrite(Front_Dir_2, LOW);
  analogWrite(PWM_Front, 200);   
}

void setup()
{
    pinMode(PWM_Rear, OUTPUT);
    pinMode(Rear_Dir_1, OUTPUT);
    pinMode(Rear_Dir_2, OUTPUT);
    
    pinMode(PWM_Front, OUTPUT);
    pinMode(Front_Dir_1, OUTPUT);
    pinMode(Front_Dir_2, OUTPUT);
}

void loop()
{
  forward();
  delay(1000);
  left();
  delay(500);
  right();
  delay(500);
  analogWrite(PWM_Front, 0);
  reverse();
  delay(1000);
}
