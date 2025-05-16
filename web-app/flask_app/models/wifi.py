# import requests
# import flask

# esp_ip = "http://192.168.3.29/status"  # Replace with ESP32's IP printed on Serial

# # payload = {
# #     'choix': 2,
# #     'move': int(False),   # convert to 1/0
# #     'type': int(False),
# #     'speed':255,
# #     'angle':200
# # }
# data_exported={}
# try:
#     response = requests.get(esp_ip,  timeout=5)  # Timeout is good practice

#     if response.status_code == 200:
#         data = response.json()
#         message = data.get("message")
#         motor_speed = data.get("Motor speed")
#         led = data.get("LED")
#         servo_angle = data.get("Servo angle")
#         data_exported=data
#         print("Status:", response.status_code)
#         print("Response:", message)
#         print("Motor Speed:", motor_speed)
#         print("LED:", led)
#         print("Servo Angle:", servo_angle)
#     else:
#         print("Failed to get valid response. Status Code:", response.status_code)
# except requests.exceptions.RequestException as e:
#  print("Error connecting to ESP32:", e)


# print("this is the dta",data_exported)

import requests

esp_ip = "http://192.168.3.29/status"

def fetch_esp_data():
    try:
        response = requests.get(esp_ip, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching ESP data: {e}")
        return None

