import requests
import flask

esp_ip = "http://192.168.116.29/data"  # Replace with ESP32's IP printed on Serial

payload = {
    'choix': 2,
    'move': int(False),   # convert to 1/0
    'type': int(False),
    'speed':255,
    'angle':200
}
try:
    response = requests.post(esp_ip, data=payload, timeout=5)  # Timeout is good practice

    if response.status_code == 200:
        data = response.json()
        message = data.get("message")
        motor_speed = data.get("Motor speed")
        led = data.get("LED")
        servo_angle = data.get("Servo angle")

        print("Status:", response.status_code)
        print("Response:", message)
        print("Motor Speed:", motor_speed)
        print("LED:", led)
        print("Servo Angle:", servo_angle)
    else:
        print("Failed to get valid response. Status Code:", response.status_code)

except requests.exceptions.RequestException as e:
 print("Error connecting to ESP32:", e)