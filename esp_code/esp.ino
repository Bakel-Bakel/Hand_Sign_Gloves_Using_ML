#include <WiFi.h>

/* WiFi credentials */
const char* ssid = "smartgloves";
const char* password = "smartgloves";

/* Raspberry Pi server settings */
const char* host = "sg.local"; // Example: "192.168.1.100" or "raspberrypi.local"
const uint16_t port = 1234; // Must match the server port on Pi

/* Create a Hardware Serial Port */
HardwareSerial SerialPort(2); // Use UART2 (RX2=GPIO16, TX2=GPIO17)

WiFiClient client;

void setup() {
  // Begin Serial for monitoring (debug to laptop)
  Serial.begin(115200);
  delay(1000);

  // Begin Serial2 for Arduino Nano connection
  SerialPort.begin(38400, SERIAL_8N1, 16, 17); // 38400 baud, RX=16, TX=17
  delay(1000);

  Serial.println("ESP32 Booting...");

  // Connect to WiFi
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Connect to Raspberry Pi server
  Serial.print("Connecting to Raspberry Pi server at ");
  Serial.print(host);
  Serial.print(":");
  Serial.println(port);

  while (!client.connect(host, port)) {
    delay(500);
    Serial.print("-");
  }
  Serial.println("\nConnected to Raspberry Pi server!");
}

void loop() {
  // Check if data available from Arduino Nano
  if (SerialPort.available()) {
    String data = SerialPort.readStringUntil('\n');
    data.trim(); // Remove any whitespace or \r

    // Send to Raspberry Pi server
    if (client.connected()) {
      client.println(data);
      Serial.println("Forwarded to Pi: " + data); // Optional debug
    } else {
      Serial.println("Disconnected from Pi, trying to reconnect...");
      reconnectToServer();
    }
  }
}

void reconnectToServer() {
  // Try to reconnect to server if connection lost
  while (!client.connect(host, port)) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nReconnected to Raspberry Pi server!");
}