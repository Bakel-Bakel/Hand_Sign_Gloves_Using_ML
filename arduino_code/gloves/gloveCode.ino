#include "I2Cdev.h"
#include "MPU6050.h"
#include <Wire.h>

/* MPU6050 Setup */
MPU6050 mpu;

#define OUTPUT_READABLE_ACCELGYRO
//#define OUTPUT_BINARY_ACCELGYRO

int16_t ax, ay, az;
int16_t gx, gy, gz;

int16_t ax0, ay0, az0;
int16_t gx0, gy0, gz0;

bool calibrated = false;
bool blinkState;

/* Flex Sensors Setup */
const int flexPins[5] = {A0, A1, A2, A3, A6};
int flexValues[5];

void setup() {
  /* Start Wire (I2C) and Serial */
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif

  Serial.begin(38400);

  /* Setup MPU6050 */
  Serial.println("Initializing MPU...");
  mpu.initialize();
  Serial.println("Testing MPU6050 connection...");
  if (mpu.testConnection() == false) {
    Serial.println("MPU6050 connection failed");
    while (true);
  } else {
    Serial.println("MPU6050 connection successful");
  }

  Serial.println("Updating internal sensor offsets...\n");
  mpu.setXAccelOffset(0);
  mpu.setYAccelOffset(0);
  mpu.setZAccelOffset(0);
  mpu.setXGyroOffset(0);
  mpu.setYGyroOffset(0);
  mpu.setZGyroOffset(0);

  Serial.print("\t");
  Serial.print(mpu.getXAccelOffset());
  Serial.print("\t");
  Serial.print(mpu.getYAccelOffset());
  Serial.print("\t");
  Serial.print(mpu.getZAccelOffset());
  Serial.print("\t");
  Serial.print(mpu.getXGyroOffset());
  Serial.print("\t");
  Serial.print(mpu.getYGyroOffset());
  Serial.print("\t");
  Serial.print(mpu.getZGyroOffset());
  Serial.print("\n");

  /* Setup Flex Sensor Pins */
  for (int i = 0; i < 5; i++) {
    pinMode(flexPins[i], INPUT);
  }

  pinMode(LED_BUILTIN, OUTPUT);

  delay(1000); // Wait a bit for MPU6050 to stabilize

  /* Calibrate Starting Position */
  Serial.println("Calibrating table position...");
  mpu.getMotion6(&ax0, &ay0, &az0, &gx0, &gy0, &gz0);
  calibrated = true;
  Serial.println("Calibration complete!");

  Serial.println("Flex + Motion Data Output Ready!");
}

void loop() {
  /* Read Flex Sensor Values */
  for (int i = 0; i < 5; i++) {
    flexValues[i] = analogRead(flexPins[i]);
  }

  /* Read IMU Values */
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  if (calibrated) {
    int16_t deltaAx = ax - ax0;
    int16_t deltaAy = ay - ay0;
    int16_t deltaAz = az - az0;
    int16_t deltaGx = gx - gx0;
    int16_t deltaGy = gy - gy0;
    int16_t deltaGz = gz - gz0;

    /* Output all Flex and IMU data */
    #ifdef OUTPUT_READABLE_ACCELGYRO
      Serial.print("Flex:\t");
      for (int i = 0; i < 5; i++) {
        Serial.print(flexValues[i]);
        Serial.print("\t");
      }

      Serial.print("Δa/g:\t");
      Serial.print(deltaAx); Serial.print("\t");
      Serial.print(deltaAy); Serial.print("\t");
      Serial.print(deltaAz); Serial.print("\t");
      Serial.print(deltaGx); Serial.print("\t");
      Serial.print(deltaGy); Serial.print("\t");
      Serial.println(deltaGz);
    #endif

    /* If you want faster machine-readable output, enable binary mode above */
  }

  blinkState = !blinkState;
  digitalWrite(LED_BUILTIN, blinkState);

  delay(50); // Small delay to reduce Serial spam
}

