// Variables for function definition
const float umin = 1065; // Minimum microseconds
const float Rmax = 5309.73; // Max RPM
const float Rmin = 402.68; // Minimum RPM
const float k = 0.00283627; // Exponential parameter

// Takes in RPM and returns requiered microseconds to achieve that RPM on esc.writeMicroseconds()
float RPM_us_function(float rpm) {
  return (-1 / k) * log(1 - ((rpm - Rmin)/(Rmax - Rmin))) + umin;
}


// Operation variables
const float Rstart = 420;
const float Rend = 5300;
const float Rstep = 11; // Step between RPM

const float accel = 3500; // RPM/s
const float delay_time = (Rstep / accel) * 1000000; // Delay between RPM increments in microseconds
const int number_of_steps = ((Rend - Rstart) / Rstep) + 1;
float RPM_us_array[number_of_steps];


// Precalculation of us
int i = 0;
void pre_calc() {
  for (float rpm = Rstart; rpm <= Rend; rpm = rpm + Rstep) {
    float us = RPM_us_function(rpm);
    RPM_us_array[i] = us;
    i ++;
  }
}

// Motor and operation function
# include <Servo.h>
Servo esc;

void accelerator() {
  for (float us : RPM_us_array) {
    esc.writeMicroseconds(us);
    delayMicroseconds(delay_time);
  }
}


// Begin operation
const int start_delay = 1000; // Delays before starting (Milliseconds)
const int end_delay = 1000; // Delays before ending (Milliseconds)
void setup() {
  Serial.begin(9600); 
  esc.attach(9, 1000, 2000);
  esc.writeMicroseconds(0);

  // esc.writeMicroseconds(RPM_us_function(2718));
  // Serial.println(RPM_us_function(2718));
  
  pre_calc();
  delay(start_delay);
  accelerator();
  delay(end_delay);
}

void loop() {
  esc.writeMicroseconds(0);
}
