#include "I2Cdev.h"
#include "MPU6050.h"
#include "MadgwickAHRS.h"
#include <Wire.h>

/* MPU6050 Setup */
MPU6050 mpu;
Madgwick filter;

int16_t ax, ay, az;
int16_t gx, gy, gz;

float pitch0, roll0, yaw0;
bool calibrated = false;
bool blinkState;

/* Flex Sensors Setup */
const int flexPins[5] = {A0, A1, A2, A3, A6};
int flexValues[5];

unsigned long lastUpdate = 0;
float deltat = 0.0f; // Time between updates

void setup() {
  Wire.begin();
  Serial.begin(38400); // Serial for TX to ESP32

  /* Setup MPU6050 */
  mpu.initialize();
  if (!mpu.testConnection()) {
    while (1); // Halt if no MPU6050
  }

  /* Setup Flex Sensor Pins */
  for (int i = 0; i < 5; i++) {
    pinMode(flexPins[i], INPUT);
  }

  pinMode(LED_BUILTIN, OUTPUT);

  delay(1000);

  /* Initialize Madgwick Filter */
  filter.begin(100); // Assuming 100Hz update rate

  /* Calibrate starting orientation */
  calibrateIMU();
}

void loop() {
  updateIMU();

  /* Read Flex Sensor Values */
  for (int i = 0; i < 5; i++) {
    flexValues[i] = analogRead(flexPins[i]);
  }

  /* Get orientation */
  float roll = filter.getRoll();
  float pitch = filter.getPitch();
  float yaw = filter.getYaw();

  /* Calculate relative orientation */
  float deltaRoll = roll - roll0;
  float deltaPitch = pitch - pitch0;
  float deltaYaw = yaw - yaw0;

  /* Send flex + orientation as comma-separated values */
  for (int i = 0; i < 5; i++) {
    Serial.print(flexValues[i]);
    Serial.print(",");
  }

  Serial.print(deltaRoll, 2); // 2 decimal points
  Serial.print(",");
  Serial.print(deltaPitch, 2);
  Serial.print(",");
  Serial.println(deltaYaw, 2); // Ends the line with \n

  blinkState = !blinkState;
  digitalWrite(LED_BUILTIN, blinkState);

  delay(10); // Faster update
}

/* ---- Helper Functions ---- */

void calibrateIMU() {
  float sumPitch = 0, sumRoll = 0, sumYaw = 0;
  int samples = 50;

  for (int i = 0; i < samples; i++) {
    updateIMU();
    sumRoll += filter.getRoll();
    sumPitch += filter.getPitch();
    sumYaw += filter.getYaw();
    delay(20);
  }

  roll0 = sumRoll / samples;
  pitch0 = sumPitch / samples;
  yaw0 = sumYaw / samples;
}

void updateIMU() {
  unsigned long now = micros();
  deltat = (now - lastUpdate) / 1000000.0f;
  lastUpdate = now;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Convert raw gyro to deg/s
  float gxD = gx / 131.0;
  float gyD = gy / 131.0;
  float gzD = gz / 131.0;

  // Convert raw accel to g
  float axG = ax / 16384.0;
  float ayG = ay / 16384.0;
  float azG = az / 16384.0;

  // Update Madgwick filter
  filter.updateIMU(gxD, gyD, gzD, axG, ayG, azG);
}