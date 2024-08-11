// Variables for function definition
const float umin = 1065; // Minimum microseconds
const float Rmax = 5309.73; // Max RPM
const float Rmin = 402.68; // Minimum RPM
const float k = 0.00283627; // Exponential parameter

// Variables for linear correction of acceleration
const float m = 1.16896; // Slope
const float b = -12.66475; // y intercept

// Variables for Nextion messages
const String waitMSG = "Waiting for Arduino...";
const String accelMSG = "Accelerating...";
const String holdMSG = "Holding at Final RPM...";
const String finishMSG = "Finished!";

// Takes in RPM and returns requiered microseconds to achieve that RPM on esc.writeMicroseconds()
float RPM_us_function(float rpm) {
  return (-1 / k) * log(1 - ((rpm - Rmin)/(Rmax - Rmin))) + umin;
}


// Operation variables
int RPMstart;
int RPMend;
long end_delay; // Milliseconds before ending
// Expected acceleration
float accel_e; // RPM/s


// Motor and accelerator function
# include <Servo.h>
Servo esc;

void accelerator() {
  // Calculation of acceleration and us
  const int RPMstep = 3; // Step between RPM
  float accel = (accel_e - b) / m; // Linear correction for acceleration in RPM/s
  const float delay_time = (RPMstep / accel) * 1000000; // Delay between RPM increments in microseconds
  const int number_of_steps = ((RPMend - RPMstart) / RPMstep) + 1;
  float RPM_us_array[number_of_steps]; // Array for precalculated us
  
  // Precalculation of us
  int i = 0;
  for (float rpm = RPMstart; rpm <= RPMend; rpm = rpm + RPMstep) {
    float us = RPM_us_function(rpm);
    RPM_us_array[i] = us;
    i ++;
  }

  // Accelerating motor
  for (float us : RPM_us_array) {
    esc.writeMicroseconds(us);
    delayMicroseconds(delay_time);
  }
}

// Nextion functions
void print2Nextion(String str) {
  Serial.print(str);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
}

void readOperationVariables(String str){
  int space1_loc = str.indexOf(",");
  int space2_loc = str.indexOf(",", space1_loc + 1);
  int space3_loc = str.indexOf(",", space2_loc + 1);

  String RPMstartStr = str.substring(0, space1_loc);
  String RPMendStr = str.substring(space1_loc + 1, space2_loc);
  String end_delayStr = str.substring(space2_loc + 1, space3_loc);
  String accel_eStr = str.substring(space3_loc + 1, str.length());

  RPMstart = RPMstartStr.toInt();
  RPMend = RPMendStr.toInt();
  end_delay = end_delayStr.toInt();
  accel_e = accel_eStr.toInt();
}

void hold(){
  print2Nextion("vis onHold,1");
    print2Nextion("vis TIMER,1");
    float start_time = millis();
    while (millis() - start_time <= end_delay)
    { 
      float remaining = (end_delay + start_time - millis()) / 1000;
      print2Nextion("TIMER.txt=\"" + String(remaining) + " s\"");
    }
    esc.writeMicroseconds(0);
    print2Nextion("TIMER.txt=\"0.00 s\"");
}

// Begin operation
const int start_delay = 1000; // Milliseconds before starting
void setup() {
  Serial.begin(9600); 
  esc.attach(9, 1000, 2000);
  esc.writeMicroseconds(0);

  delay(start_delay);
}

void loop() {
  if (Serial.available() > 0){
    print2Nextion("statusMSG.txt=\"" + waitMSG + "\"");
    delay(100);
    
    String MSG = Serial.readString();
    readOperationVariables(MSG);
    
    print2Nextion("statusMSG.txt=\"" + accelMSG + "\"");
    accelerator();

    print2Nextion("statusMSG.txt=\"" + holdMSG + "\"");
    hold();

    print2Nextion("statusMSG.txt=\"" + finishMSG + "\"");
    print2Nextion("vis BACK,1");
  }
}