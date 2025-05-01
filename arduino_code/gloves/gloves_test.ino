#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>


//Adafruit_MPU6050 mpu;

void setup() { 
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A6, INPUT);
  Serial.begin(9600);
  

  Serial.println("Testing all five fives\nA0    A1    A2    A3    A6  ");
  delay(100);
}

void loop() {
  
int A6_ = analogRead(A6);
int A3_ = analogRead(A3);
int A2_ = analogRead(A2);
int A1_ = analogRead(A1);
int A0_ = analogRead(A0);
  
Serial.print(A0_);
Serial.print(A1_);
Serial.print(A2_);
Serial.print(A3_);
Serial.println(A6_); // Ends the line

delay(100);




}