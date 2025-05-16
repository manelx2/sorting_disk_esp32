#include <ESP32Servo.h>
// Define LED pins
const int led1 = 4;
const int led2 = 5;
const int led3 = 19;
const int speedPin = 14;  
const int directionPin = 27;
  
//----------------------
int ledChoice = 1;
bool move = false; 
bool type= false; 
int speed=0;
int angle=0;
//----------------------
// servo motor 
Servo myServo;             // Servo object
const int servoPin = 18;   // Choose an unused PWM-capable pin
int servoAngle = 0;        // Default angle

//Wifi
#include <WiFi.h>
#include <WebServer.h>
const char* ssid = "Connexion ";
const char* password = "12345678";

WebServer server(80);
void handlePost() {
  if (server.hasArg("choix") && server.hasArg("move") && server.hasArg("type")) {
    ledChoice = server.arg("choix").toInt();
    move = server.arg("move").toInt();     // Convert "0"/"1" to bool
    type = server.arg("type").toInt();
    speed= server.arg("speed").toInt();
    angle= server.arg("angle").toInt();

    Serial.printf("Received - Choix: %d, Move: %d, Type: %d ,speed: %d , Angle: %d\n",ledChoice, move, type, speed, angle);
    String json = "{";
    json += "\"message\":\"Data received\",";
    json += "\"Motor speed\":" + String(speed) + ",";
    json += "\"LED\":" + String(ledChoice) + ",";
    json += "\"Servo angle\":" + String(servoAngle);
    json += "}";
    server.send(200, "application/json", json);
  } else {
    server.send(400, "text/plain", "Missing parameters");
  }
  
}


// Function to control the servo
void controlServo(bool move, bool type) {
  if (!move && type) {
    servoAngle = angle;  
  } else {
    servoAngle = 0;   
  }
  myServo.write(servoAngle);
  delay(1000);
  myServo.write(0);
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
    analogWrite(speedPin, speed);     // Set motor speed
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
 //---------------------------
  myServo.attach(servoPin); 
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
  controlServo(move,type);
  //controlServo(move, type);
  delay(1000); 
  
// Delay to prevent rapid changes
}
