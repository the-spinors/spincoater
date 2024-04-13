# include <Servo.h>
//declaración de variables
const float volt_config = 5; //selección de configuración de voltaje
const float speed = 200; //aceleración angular
const float RPM_start=100; //rpm de inicio para la configuración
const float RPM_stop=2000; //rpm de finalización para la configuración
int main_delay = 3;//segundos de rotación a máxima velocidad

float RPM_min=0; //rpm mínima de la configuración
float RPM_max=0; //rpm máxima de la configuración

int microseconds_min = 1110; //microseconds para alcanzar el mínimo
int microseconds_max = 2000; //microseconds para alcanzar el máximo

int microseconds_start = 0; //microseconds de inicio para configuración
int microseconds_stop = 0; //microseconds de finalización para la configuración

int par_delay = 0; //delay parcial

//prototipo de las funciones 
void config(); //configuración
double function(int microseconds); //función de transformación
double inverse(float rpm); //función inversa de transformación
double delay(int microseconds); //calcula el delay entre los saltos

Servo esc;

void setup() {
  Serial.begin(9600);
  esc.attach(9,1000,2000);
  config();
  microseconds_start = inverse(RPM_start);
  microseconds_stop = inverse(RPM_stop);
   for (int m = microseconds_start; m < microseconds_stop; ++m) {
    par_delay = delay(m);
    esc.writeMicroseconds(m);
    delayMicroseconds(par_delay);
  }
  esc.writeMicroseconds(microseconds_stop);
  main_delay = main_delay*1000000;
  delayMicroseconds(main_delay);
  }

void loop(){
  esc.writeMicroseconds(0);
}

//delay
double delay(int microseconds){
  int delay;
  float diff = function(microseconds+1)-function(microseconds);
  delay = (diff / speed)*1000000;
  return delay;}
//configuraciones
void config(){
  if(volt_config==4.5){
    RPM_min=181.45;
    RPM_max=4724.41;
  }
  if(volt_config==5){
    RPM_min=419.09;
    RPM_max=5309.73;
  }
  if(volt_config==8){
    RPM_min=1470.59;
    RPM_max=8571.43;
  }}

//funciones
double function(int microseconds){
  float rpm;
  if(volt_config==4.5){
    rpm = microseconds;
  }
  if(volt_config==5){
    rpm = microseconds;
  }
  if(volt_config==8){
    rpm = microseconds;
  }
  return rpm;}
//inversas
double inverse(float rpm){
  int microseconds;
  if(volt_config==4.5){
    microseconds = rpm;
  }
  if(volt_config==5){
    microseconds = rpm;
  }
  if(volt_config==8){
    microseconds = rpm;
  }
  return microseconds;
  }
//end code
