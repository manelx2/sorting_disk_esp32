#include <ESP32Servo.h>
// Define LED pins
const int led1 = 2;
const int led2 = 4;
const int led3 = 5;
const int speedPin = 14;  
const int directionPin = 27;
  
//----------------------
int ledChoice = 1;
bool move = false; 
bool type= true; 
//----------------------
// servo motor 
Servo myServo;             // Servo object
const int servoPin = 18;   // Choose an unused PWM-capable pin
int servoAngle = 0;        // Default angle

//Wifi
#include <WiFi.h>
#include <WebServer.h>
const char* ssid = "wifi_name";
const char* password = "password";

WebServer server(80);
void handlePost() {
  if (server.hasArg("choix") && server.hasArg("move") && server.hasArg("type")) {
    ledChoice = server.arg("choix").toInt();
    move = server.arg("move").toInt();     // Convert "0"/"1" to bool
    type = server.arg("type").toInt();

    Serial.printf("Received - Choix: %d, Move: %d, Type: %d\n",ledChoice, move, type);
    server.send(200, "text/plain", "Data received");
  } else {
    server.send(400, "text/plain", "Missing parameters");
  }
  
}


// Function to control the servo
void controlServo(bool move, bool type) {
  if (!move && type) {
    servoAngle = 90;  // Turn to 90° if condition is met
  } else {
    servoAngle = 0;   // Stay or return to 0°
  }
  
  myServo.write(servoAngle);
  Serial.print("Servo Angle: ");
  Serial.println(servoAngle);

}

// Function to control LEDs
void lightUpLED(int choice) {
  // Turn off all LEDs first
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);

  // Turn on the selected LED
  if (choice == 1) {
    digitalWrite(led1, HIGH);
  } else if (choice == 2) {
    digitalWrite(led2, HIGH);
  } else if (choice == 3) {
    digitalWrite(led3, HIGH);
  }
}
// Function to control motor
void controlMotor(bool move) {
 if (move) {
    digitalWrite(directionPin, HIGH); // Set direction forward
    analogWrite(speedPin, 200);     // Set motor speed
  } else {
    analogWrite(speedPin, 0);         // Stop motor
  }
}

void setup() {
  // Set pins as outputs
  Serial.begin(9600);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(speedPin, OUTPUT);
  pinMode(directionPin, OUTPUT);
 //----------------------------
  myServo.setPeriodHertz(50);          // Standard 50Hz for servo
  myServo.attach(servoPin, 500, 2400); // Typical pulse width range for servos (adjust if needed)
  myServo.write(servoAngle);
  //-------------------------wifi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nConnected to WiFi!");
  Serial.println(WiFi.localIP());  // Note this IP for the Python script

  server.on("/data", HTTP_POST, handlePost);
  server.begin();
  

}

void loop() {

 server.handleClient();
  // Call the function with the chosen value
  lightUpLED(ledChoice);
  controlMotor(move);
  //controlServo(move, type);
  delay(1000); 
  
// Delay to prevent rapid changes
}
