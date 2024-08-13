// Signal pin
int signal_pin = 10;
int motor_pin = 9;

// Motor
# include <Servo.h>
Servo esc;

void setup() {
  pinMode(signal_pin, OUTPUT);
  esc.attach(motor_pin, 1000, 2000);
  esc.writeMicroseconds(0);

  for (int us = 1100; us <= 2000; us = us + 100) {
    digitalWrite(signal_pin, HIGH);
    esc.writeMicroseconds(us);
    delay(2000);

    esc.writeMicroseconds(0);
    digitalWrite(signal_pin, LOW);
    delay(2000);
  }

  delay(5000);
  esc.writeMicroseconds(0);
}

void loop() {
  digitalWrite(signal_pin, LOW);
}
