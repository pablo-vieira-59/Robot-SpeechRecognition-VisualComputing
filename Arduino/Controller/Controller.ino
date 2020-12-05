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
int delayTime = 50;

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
      motorFoward();
      delay(delayTime);
      motorStop();
    }
    
    if (req == "a") {
      motorLeft();
      delay(delayTime);
      motorStop();
    }

    if (req == "s") {
      motorBackward();
      delay(delayTime);
      motorStop();
    }
    
    if (req == "d") {
      motorRight();
      delay(delayTime);
      motorStop();
    }
    
    if (req == "r") {
      float sensor = sensorDistance();
      Serial.println(sensor);
    }

    if (req == "l"){
      ledControl();
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

void motorFoward() {
  analogWrite(motor_r1, motorPower);
  digitalWrite(motor_r2, LOW);
  analogWrite(motor_l1, motorPower);
  digitalWrite(motor_l2, LOW);
}

void motorBackward() {
  digitalWrite(motor_r1, LOW);
  analogWrite(motor_r2, motorPower);
  digitalWrite(motor_l1, LOW);
  analogWrite(motor_l2, motorPower);
}

void motorRight() {
  digitalWrite(motor_r1, LOW);
  analogWrite(motor_r2, motorPower);
  analogWrite(motor_l1, motorPower);
  digitalWrite(motor_l2, LOW);
}

void motorLeft() {
  analogWrite(motor_r1, motorPower);
  digitalWrite(motor_r2, LOW);
  digitalWrite(motor_l1, LOW);
  analogWrite(motor_l2, motorPower);
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

void clearSerial(){
  while(Serial.available()>0){
    Serial.read();
    delay(15);
  }
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
