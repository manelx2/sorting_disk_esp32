import cv2
import numpy as np
import requests
esp_ip = "http://192.168.116.29/data"  
dashboard_ip= "http://127.0.0.1:5000"

# variable to be read from server
angle=0
speed=0
# ---------------------------------------------------------------------


# Start camera
cap = cv2.VideoCapture(1)

# Define HSV ranges
lower_green = np.array([35, 60, 60])
upper_green = np.array([85, 255, 255])

lower_blue = np.array([110, 100, 30])
upper_blue = np.array([135, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Morphological cleanup
    kernel = np.ones((5, 5), np.uint8)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

    # Process masks
    def detect_circle(mask, color_name, bgr_color, label_value):
        part = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                                   param1=50, param2=30, minRadius=20, maxRadius=100)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for (x, y, r) in circles[0, :1]:  # Only first circle
                cv2.circle(output, (x, y), r, bgr_color, 3)
                cv2.putText(output, f"{color_name} Circle", (x - 40, y - r - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, bgr_color, 2)
            return True, label_value
        return False, None

    # Detection logic
    found_blue, blue_label = detect_circle(mask_blue, "Blue", (255, 0, 0), 1)
    found_green, green_label = detect_circle(mask_green, "Green", (0, 255, 0), 2)

    # Priority: Blue > Green (change as needed)
    if found_blue:
        disk_color = blue_label
        no_disk = False
    elif found_green:
        disk_color = green_label
        no_disk = False
    else:
        disk_color = 3
        no_disk = True

    # Debug info on screen
    cv2.putText(output, f"disk_color = {disk_color}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(output, f"no_disk = {no_disk}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Show output
    cv2.imshow("Disk Detection", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    angle=100
    speed=255
    #----------------------------------------------------------this is where we connect to the dashbord-----------------------------
    payload2 = {
        'LedChoice':led,
        'move': int(no_disk),   
        'type': int(disk_color==2),
        'speed':motor_speed,
        'angle':servo_angle
    }
    try:
        response2=requests.post(dashboard_ip,data2=payload2, timeout=5)

        if response2.status_code == 200:
            speed = data2.get("Motor speed")
            angle = data2.get("Servo angle")

            print("dashboard speed:", speed)
            print("dashboard speed:", angle)
        else:
            print("Failed to get valid response. Status Code:", response2.status_code)

    except requests.exceptions.RequestException as e:
        print("Error connecting to dashboard:", e)
    #--------------------------------------------------------esp32-----------------------------------------
    payload = {
        'choix':disk_color,
        'move': int(no_disk),   # convert to 1/0
        'type': int(disk_color==2),
        'speed':speed,
        'angle':angle
    }
    #----------------------------------------------           ->     ----------------------------------
    #----------------------------------------------sort-disk  <-  esp----------------------------------
    try:
        response = requests.post(esp_ip, data=payload, timeout=5)  

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
    
cap.release()
cv2.destroyAllWindows()
