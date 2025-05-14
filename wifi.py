import requests

esp_ip = "http://IP/data"  # Replace with ESP32's IP printed on Serial

payload = {
    'choix': 1,
    'move': int(False),   # convert to 1/0
    'type': int(False)
}

response = requests.post(esp_ip, data=payload)
print("Status:", response.status_code)
print("Response:", response.text)
