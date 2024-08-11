const String waitMSG = "Waiting for Arduino...";
const String accelMSG = "Accelerating...";
const String holdMSG = "Holding at Final RPM...";
const String finishMSG = "Finished!";

int LED = 9;
int RPMstart;
int RPMend;
int end_delay;
int accel_r;

void endCode() {
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
  String accel_rStr = str.substring(space3_loc + 1, str.length());

  RPMstart = RPMstartStr.toInt();
  RPMend = RPMendStr.toInt();
  end_delay = end_delayStr.toInt();
  accel_r = accel_rStr.toInt();
}

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {
  delay(100);
  if (Serial.available() > 0){
    Serial.print("statusMSG.txt=\"" + waitMSG + "\"");
    endCode();
    delay(100);
    
    String MSG = Serial.readString();
    readOperationVariables(MSG);
  }
}
