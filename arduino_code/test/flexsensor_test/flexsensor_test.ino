// www.sciencebuddies.org

// declare variables
int sensorpin = A0;  // sensor pin
int sensor;          // sensor readings

void setup() {
  // put your setup code here, to run once:
  // initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  // read sensor value
  sensor = analogRead(sensorpin);
  // print sensor value
  Serial.println(sensor);
  // turn on LEDs if sensor reading
  // exceeds a certain threshold
  
}
