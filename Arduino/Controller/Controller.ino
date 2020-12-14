#include "Headers.h"

// Definindo Led de Estado do Microfone
#define led_pin 2

// Definindo Entrada do Motor Esquerdo
#define motor_l1 5
#define motor_l2 6

// Definindo Entrada do Motor Direto
#define motor_r1 11
#define motor_r2 10

// Definindo Entrada do Sensor Ultrasonico
#define trigger 7
#define echo 8 

// Definindo Força do Motor - PWM
#define motorPower 255

// Definindo delayTime de Espera entre Estados
int delayTime = 30;

// Definindo estado do requerimento da comunicação serial
String req = "";

// Inicialização
void setup() {
  // Inicia a comunicação Serial
  Serial.begin(115200);

  // Define Entradas e Saidas
  pinMode(trigger,OUTPUT);
  pinMode(echo,INPUT);
  pinMode(led_pin,OUTPUT);

  // Inicia Estado do Sensor
  digitalWrite(trigger,LOW);
}

// Loop Principal
void loop() {
  // Verifica se existe novos dados no buffer Serial
  if (Serial.available() > 0) {
    
    // Lê Buffer Serial - Valor da letra recebida em ASCII
    req = getMessage();

    if (req == "w") {
      controlMotors(255,0,255,0,25);
    }
    
    if (req == "a") {
      controlMotors(255,0,0,255,25);
    }

    if (req == "s") {
      controlMotors(0,255,0,255,25);
    }
    
    if (req == "d") {
      controlMotors(0,255,255,0,25);
    }
    
    if (req == "sensor") {
      float sensor = sensorDistance();
      String str = String(sensor);
      clearSerial();
      Serial.println(str);
    }

    if (req == "l"){
      ledControl();
    }

    if (req == "backward"){
      controlMotors(0,255,0,255,800);
    }

    if (req == "forward"){
      controlMotors(255,0,255,0,800);
    }

    if (req == "left"){
      controlMotors(255,0,0,255,300);
    }

    if (req == "right"){
      controlMotors(0,255,255,0,300);
    }
  }
}

double sensorDistance(){
  digitalWrite(trigger,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger,LOW);
  double pulseDelta = pulseIn(echo, HIGH);
  double dist = (pulseDelta / 29.4)/2;
  return dist;
}

void controlMotors(int powerA, int powerB, int powerC, int powerD, int time){
  analogWrite(motor_r1, powerA);
  digitalWrite(motor_r2, powerB);

  analogWrite(motor_l1, powerC);
  digitalWrite(motor_l2, powerD);
  delay(time);
  motorStop();
}

void motorStop() {
  digitalWrite(motor_r1, LOW);
  digitalWrite(motor_r2, LOW);
  digitalWrite(motor_l1, LOW);
  digitalWrite(motor_l2, LOW);
}

bool ledControl(){
  digitalWrite(led_pin, HIGH);
  delay(1000);
  digitalWrite(led_pin, LOW);
}

String getMessage(){
  char currentByte = "";
  String message = "";
  while(Serial.available() > 0){
    currentByte = Serial.read();
    if(currentByte != '\n'){
      message.concat(currentByte);
    }
    delay(15);
  }
  return message;
}

void clearSerial(){
  while(Serial.available()>0){
    Serial.read();
  }
  delay(15);
}
