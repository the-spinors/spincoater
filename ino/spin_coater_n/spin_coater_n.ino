// Variables for function definition
const float umin = 1065; // Minimum microseconds
const float Rmax = 5309.73; // Max RPM
const float Rmin = 402.68; // Minimum RPM
const float k = 0.00283627; // Exponential parameter

// Variables for linear correction of acceleration
const float m = 1.16896; // Slope
const float b = -12.66475; // y intercept

// Takes in RPM and returns requiered microseconds to achieve that RPM on esc.writeMicroseconds()
float RPM_us_function(float rpm) {
  return (-1 / k) * log(1 - ((rpm - Rmin)/(Rmax - Rmin))) + umin;
}


// Operation variables
const float RPMstart = 420;
const float RPMend = 5300;
const float RPMstep = 3; // Step between RPM
// Expected acceleration
float accel_r = 7000; // RPM/s

float accel = (accel_r - b) / m; // Linear correction for acceleration in RPM/s
const float delay_time = (RPMstep / accel) * 1000000; // Delay between RPM increments in microseconds
const int number_of_steps = ((RPMend - RPMstart) / RPMstep) + 1;
float RPM_us_array[number_of_steps]; // Array for precalculated us


// Precalculation of us
int i = 0;
void pre_calc() {
  for (float rpm = RPMstart; rpm <= RPMend; rpm = rpm + RPMstep) {
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
const int end_delay = 3000; // Delays before ending (Milliseconds)
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