#include <Servo.h>

Servo myservo;

float pos = 0;

void setup() {
  Serial.begin(9600);
  myservo.attach(2); 
}



void loop() {
  if(Serial.available() > 0){
    String message = getMessage();
    int val = message.toInt();
    Serial.println(message);
    pos = map(val, -100, 100, 0.0, 180.0);
    //clearSerial();
    Serial.write("f \n");
  }
  myservo.write(pos);
  delay(15);
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
