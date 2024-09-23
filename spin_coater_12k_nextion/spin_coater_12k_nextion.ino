// Motor and accelerator function
#include <Servo.h>
Servo esc;

// Data for acceleration calculation
int data_us_5v[30] = {1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000};

float data_RPM_5v[30] = {522.7276699170616, 542.3137048451654, 550.2536078130512, 567.9801042038741, 579.8876739248126, 591.0798321533913, 600.9565864935408, 617.2111546286206, 631.7594094031758, 635.3845412115163, 656.9814146494098, 758.7606423309594, 1024.9489361367937, 1620.2232045745675, 2260.385813017392, 2877.087027804731, 3177.2010495414747, 3459.008601524048, 3604.1066426882658, 3802.305893735386, 3928.419287903149, 4166.666666666667, 4271.410691936349, 4471.900700578738, 4513.549694272587, 4389.639788621113, 4769.9248120300745, 4691.698387819078, 5174.970596757973, 5076.156665139717};

int data_us_12v[25] = {1080, 1085, 1090, 1095, 1100, 1105, 1110, 1115, 1130, 1132, 1133, 1134, 1136, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 2000};
        
float data_RPM_12v[25] = {3758.423180592992, 3894.428152492668, 4055.7777164920017, 4195.81240317356, 4334.946365158512, 4449.157325213019, 4565.227751713036, 4687.5, 5074.009390746678, 5123.837019028473, 5132.625994694959, 5161.8879205086105, 5228.7651373017225, 6521.75454104431, 8047.929300301215, 9132.44124842464, 9764.132925897631, 10371.767241379312, 10859.755140480302, 11407.02776664612, 11301.83950442143, 11842.228548835876, 12500.027126853847, 12615.724255804016, 12511.62250116225};


// Operation variables
const int rpm_step = 10; // Step between RPM
float accel;
int RPM_INIT;
int RPM_FINAL;
float delay_time; // Delay between RPM increments in microseconds
float hold_time;
int number_steps;


// Precalculate arrays
int us_rpm_5v(int rpm){
  int us_p;
  for(int i = 0; i <= 28; i++){
    if(rpm <= data_RPM_5v[i+1] && rpm > data_RPM_5v[i]){
      int y1 = data_RPM_5v[i+1];
      int y0 = data_RPM_5v[i];
      int x1 = data_us_5v[i+1];
      int x0 = data_us_5v[i];     
      float m = (y1 - y0)/(x1 - x0);
      int us_p = (rpm - y0)/(m) + x0;
      return us_p;
    }
  }
}


int us_rpm_12v(int rpm){
  int us_p;
  for(int i = 0; i <= 23; i++){
    if(rpm <= data_RPM_12v[i+1] && rpm > data_RPM_12v[i]){
      int y1 = data_RPM_12v[i+1];
      int y0 = data_RPM_12v[i];
      int x1 = data_us_12v[i+1];
      int x0 = data_us_12v[i];
      float m = (y1 - y0)/(x1 - x0);
      int us_p = (rpm - y0)/(m) + x0;
      return us_p;
    } 
  }
}


// Accelerate
void accelerate(){
    // Calculate from Nextion inputs.
    float delay_time = (rpm_step / accel) * 1000000; // Delay between RPM increments in microseconds
    int number_steps = ((RPM_FINAL - RPM_INIT) / rpm_step) + 1;

    // Precalculation
    int j = 0;
    int m = 0;
    int us[number_steps]; // Array for precalculated
    for(int rpm = RPM_INIT ; rpm <= RPM_FINAL; rpm = rpm + rpm_step){
      if(rpm <= 4400){
        us[j] = us_rpm_5v(rpm);
        m++;
      }
      else{
        us[j] = us_rpm_12v(rpm);
      }
      
      j++;
  
    }
  
    //Aceleration
    esc.writeMicroseconds(1080);
    delay(5000);
    
    for(int i = 0; i <= m - 1; i++){
      esc.writeMicroseconds(us[i]);
      delayMicroseconds(delay_time);
    }

    if (RPM_FINAL > 4400){
      esc.writeMicroseconds(us[m]);
      delay(29);
      digitalWrite(50, HIGH);

      //Acceleration rough after commutation
      for(int j = m + 1; j <= number_steps - 1   ; j++){
      esc.writeMicroseconds(us[j]);
      delayMicroseconds(delay_time);
      }
    }
}


// Nextion
// Variables for Nextion messages
const String waitMSG = "Waiting for Arduino...";
const String accelMSG = "Accelerating...";
const String holdMSG = "Holding at Final RPM...";
const String finishMSG = "Finished!";


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

  String RPM_INITStr = str.substring(0, space1_loc);
  String RPM_FINALStr = str.substring(space1_loc + 1, space2_loc);
  String hold_timeStr = str.substring(space2_loc + 1, space3_loc);
  String accelStr = str.substring(space3_loc + 1, str.length());

  RPM_INIT = RPM_INITStr.toInt();
  RPM_FINAL = RPM_FINALStr.toInt();
  hold_time = hold_timeStr.toInt() * 1000;
  accel = accelStr.toInt();
}


void hold(){
  print2Nextion("vis onHold,1");
    print2Nextion("vis TIMER,1");
    float start_time = millis();
    const float bias = 0.1;
    while (millis() - start_time <= hold_time)
    { 
      float remaining = (hold_time + start_time - millis()) / 1000;
      print2Nextion("TIMER.txt=\"" + String(remaining) + " s\"");
    }
    
    digitalWrite(50, LOW);
    esc.writeMicroseconds(1000);
    // delay(2000);
    // esc.writeMicroseconds(0);
    print2Nextion("TIMER.txt=\"0.00 s\"");
}


// Begin operation
const int start_delay = 1000; // Milliseconds before starting
void setup() {
  pinMode(50, OUTPUT); // Relay pin
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
    accelerate();

    print2Nextion("statusMSG.txt=\"" + holdMSG + "\"");
    hold();

    print2Nextion("statusMSG.txt=\"" + finishMSG + "\"");
    print2Nextion("vis BACK,1");
  }
}
