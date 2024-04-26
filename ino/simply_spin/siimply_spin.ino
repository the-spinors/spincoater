# include <Servo.h>

// for (int us = 1065; us <= 2000; us = us + step){
   // esc.writeMicroseconds(us);
   // Serial.println(us);
   // delay(1000);
   // esc.writeMicroseconds(0);
   // delay(500);
//  }

Servo esc;

int step = 100; // us
void setup(){
  Serial.begin(9600);
  esc.attach(9, 1000, 2000);
  esc.writeMicroseconds(0);
  esc.writeMicroseconds(20005309.);
  delay(10000);
}

void loop() {
  esc.writeMicroseconds(0);

}
