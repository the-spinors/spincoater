#include <Servo.h>
Servo esc;

//data requiered to find the us
int data_us_5v[45] = {1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1100, 1100, 1150, 1150, 1200, 1250, 1250, 1300, 1350, 1350, 1400, 1450, 1450, 1500, 1550, 1550, 1600, 1650, 1650, 1700, 1700, 1750, 1750, 1800, 1800, 1850, 1850, 1900, 1900, 1950, 1950, 2000, 2000, 2000};
float data_RPM_5v[45] = {522.7276699170616, 542.3137048451654, 550.2536078130512, 567.9801042038741, 579.8876739248126, 591.0798321533913, 600.9565864935408, 617.2111546286206, 631.7594094031758, 635.3845412115163, 656.9814146494098, 707.052247297749, 758.7606423309594, 1032.3006920939783, 1024.9489361367937, 1620.2232045745675, 2293.0084959616443, 2260.385813017392, 2877.087027804731, 3181.339738745546, 3177.2010495414747, 3459.008601524048, 3647.488625485304, 3604.1066426882658, 3802.305893735386, 3925.0085999312, 3928.419287903149, 4166.666666666667, 4267.433954933955, 4271.410691936349, 4466.506751954513, 4471.900700578738, 4513.176881597934, 4513.549694272587, 4387.802350450908, 4389.639788621113, 4764.071233588977, 4769.9248120300745, 4695.896775638154, 4691.698387819078, 5176.697365602913, 5174.970596757973, 5082.5984883188285, 5078.303939532752, 5076.156665139717};

int data_us_12v[48] = {1080, 1085, 1090, 1090, 1095, 1095, 1100, 1100, 1105, 1105, 1110, 1110, 1115, 1115, 1130, 1130, 1132, 1132, 1133, 1133, 1134, 1134, 1136, 1136, 1200, 1200, 1300, 1300, 1400, 1400, 1500, 1500, 1600, 1600, 1700, 1700, 1750, 1750, 1800, 1800, 1850, 1850, 1900, 1900, 1950, 1950, 2000, 2000};
float data_RPM_12v[48] = {3758.423180592992, 3894.428152492668, 4052.2328258177313, 4055.7777164920017, 4186.698717948718, 4195.81240317356, 4326.93108560577, 4334.946365158512, 4459.185553712918, 4449.157325213019, 4570.514303338732, 4565.227751713036, 4687.595373252761, 4687.5, 5071.927075915111, 5074.009390746678, 5110.821382007823, 5123.837019028473, 5110.747370620604, 5132.625994694959, 5152.432566021747, 5161.8879205086105, 5232.6468344774985, 5228.7651373017225, 6524.58705145244, 6521.75454104431, 8042.914712133468, 8047.929300301215, 9130.503642698764, 9132.44124842464, 9744.792201748924, 9764.132925897631, 10385.77195584116, 10371.767241379312, 10869.565217391304, 10859.755140480302, 11411.828205721336, 11407.02776664612, 11297.324042807151, 11301.83950442143, 11850.492372663944, 11842.228548835876, 12476.947902259106, 12500.027126853847, 12593.321847567477, 12615.724255804016, 12500.0, 12511.62250116225};

float acc = 1500;
float RPM_INIT = 5500;
float RPM_FINAL = 5000;
const int rpm_step = 50; // Step between RPM
const float delay_time = (rpm_step / acc) * 1000000; // Delay between RPM increments in microseconds
const int number_steps = ((RPM_FINAL - RPM_INIT) / rpm_step) + 1;


int us_rpm_5v(float rpm){
  int us_p;
  for(int i = 0; i <= 43; i++){
    if(rpm <= data_RPM_5v[i+1] && rpm > data_RPM_5v[i]){
      int y1 = data_RPM_5v[i+1];
      int y0 = data_RPM_5v[i];
      int x1 = data_us_5v[i+1];
      int x0 = data_us_5v[i];     
      float m = (y1 - y0)/(x1 - x0);
      int us_p = (rpm - y0)/(m) + x0;
      //Serial.print("us_p: ");
      //Serial.println(us_p);
      return us_p;
    }
  }
  
}


int us_rpm_12v(float rpm){
  int us_p;
  for(int i = 0; i <= 46; i++){
    if(rpm <= data_RPM_12v[i+1] && rpm > data_RPM_12v[i]){
      int y1 = data_RPM_12v[i+1];
      int y0 = data_RPM_12v[i];
      int x1 = data_us_12v[i+1];
      int x0 = data_us_12v[i];
      float m = (y1 - y0)/(x1 - x0);
      int us_p = (rpm - y0)/(m) + x0;
      //Serial.print("us_p: ");
      //Serial.println(us_p);
      return us_p;
    } 
  }
  
}


void accelerator(){
  int j = 0;
  int marker = 0;
  int us[number_steps]; // Array for precalculated 

  Serial.println("Acelerator");
  Serial.println(number_steps);

  //pre-calculate us
  Serial.println("init calculation");
  for(int rpm = RPM_INIT ; rpm <= RPM_FINAL; rpm = rpm + rpm_step){
    if(rpm < 5000){
      //Serial.print(rpm);
      //Serial.print(" , ");
      //Serial.println(us_rpm_5v(rpm));
      us[j] = us_rpm_5v(rpm);
      marker ++;
    }
    else{
      //Serial.print(rpm);
      //Serial.print(" , ");
      //Serial.println(us_rpm_5v(rpm));
      us[j] = us_rpm_12v(rpm);
    }
    j++;

  }
  
  Serial.println("end calculation");
  //Serial.println(us[30]);

  //accelerate
  Serial.println("First phase of acceleration");
  Serial.println(delay_time);
  for(int i = 0; i < marker; i++){
    esc.writeMicroseconds(us[i]);
    delayMicroseconds(delay_time);
  }

  digitalWrite(52, HIGH);
  Serial.println("Second Phase of Acceleration");

  for(int j = marker ; j <= number_steps ; j++){
    esc.writeMicroseconds(us[j]);
    delayMicroseconds(delay_time);
  }
  Serial.println(us[number_steps-1]);
  Serial.println("Waiting");
  delay(3000);
  digitalWrite(52, LOW);
  esc.writeMicroseconds(0);
  Serial.println("ending");

}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  esc.attach(9, 1000, 2000);
  pinMode(52, OUTPUT);
  esc.writeMicroseconds(1000);
  delay(1000);
  accelerator(); 
  
}

void loop() {
  esc.writeMicroseconds(0);
}