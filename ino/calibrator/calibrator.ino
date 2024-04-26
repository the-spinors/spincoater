#include <Servo.h>
Servo esc;

void setup() {
  Serial.begin(9600);
  esc.attach(9, 1000, 2000);
  delay(2000);
  esc.writeMicroseconds(2000);
  delay(2000);
  esc.writeMicroseconds(1000);
  delay(2000);
}
void loop() {
  // put your main code here, to run repeatedly:

}
