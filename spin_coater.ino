# include <Servo.h>
const float E = 2.718281828459045235360287471352; // no preguntes si ya sabes
//declaración de variables
const float volt_config = 5; //selección de configuración de voltaje
const float speed = 800; //aceleración angular (en rpm/s)
const float RPM_start=100; //rpm de inicio para la configuración
const float RPM_stop=5000; //rpm de finalización para la configuración
int main_delay = 3;//segundos de rotación a máxima velocidad

float RPM_min=0; //rpm mínima de la configuración
float RPM_max=0; //rpm máxima de la configuración
float k = 0; //constante de proporcionalidad en la constante

int microseconds_min = 1110; //microseconds para alcanzar el mínimo
int microseconds_max = 2000; //microseconds para alcanzar el máximo

int microseconds_start = 0; //microseconds de inicio para configuración
int microseconds_stop = 0; //microseconds de finalización para la configuración

int par_delay = 0; //delay parcial

//prototipo de las funciones 
void config(); //configuración
double function(int microseconds); //función de transformación
double inverse(float rpm); //función inversa de transformación
double m_delay(int microseconds); //calcula el delay entre los saltos

Servo esc;

void setup() {
  Serial.begin(9600);
  Serial.println("");
  esc.attach(9,1000,2000);
  Serial.println("Start");
  config();
  microseconds_start = inverse(RPM_start);
  microseconds_stop = inverse(RPM_stop);
  for (int m = microseconds_start; m < microseconds_stop; ++m) {
    par_delay = m_delay(m);
    esc.writeMicroseconds(m);
    delay(par_delay);
    Serial.print("microseconds:");// impresión de data
    Serial.print(m);
    Serial.print(", delay:");
    Serial.print(par_delay);
    Serial.print(", RPM:");
    Serial.println(function(m));
  }
  esc.writeMicroseconds(microseconds_stop);
  main_delay = main_delay*1000;
  Serial.println("Hold");
  delay(main_delay);
  Serial.println("Clear");
  }

void loop(){
  esc.writeMicroseconds(0);
}

//delay
double m_delay(int microseconds){
  int plus = microseconds+1;
  float diff = function(plus)-function(microseconds);
  int delay_p = (diff/speed)*1000;
  return delay_p;}
//configuraciones
void config(){
  if(volt_config==4.5){
    RPM_min=181.45;
    RPM_max=4724.41;
    k=0.0067;
  }
  if(volt_config==5){
    RPM_min=419.09;
    RPM_max=5309.73;
    k=0.006806947327925002;
  }
  if(volt_config==8){
    RPM_min=1470.59;
    RPM_max=8571.43;
    k=0.007221156275187404;
  }}

//funcion
double function(int microseconds){
  float exponent = -k*(microseconds-microseconds_min); //parametro exponente de la función
  float rpm = (RPM_max-RPM_min)*(1-pow(E,exponent))+RPM_min; //función
  return rpm;}

//inversa
double inverse(float rpm){
  float logarithm = 1-((rpm-RPM_min)/(RPM_max-RPM_min)); //parametro logaritmo de la función inversa
  int microseconds = -(log(logarithm)/k)+microseconds_min; //función inversa
  return microseconds;}
//end code
