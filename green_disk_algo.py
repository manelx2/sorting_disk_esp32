import cv2
import numpy as np

# Start camera (0 = default webcam)
cap = cv2.VideoCapture(0)

# Define green color range in HSV (tune if needed)
lower_green = np.array([35, 60, 60])
upper_green = np.array([85, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Optionally clean mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Extract green parts
    green_part = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert to gray and blur
    gray = cv2.cvtColor(green_part, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=50, param2=30, minRadius=20, maxRadius=100)

    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :]:
            cv2.circle(output, (x, y), r, (0, 255, 0), 3)
            cv2.putText(output, "Green Circle", (x - 40, y - r - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show result
    cv2.imshow("Green Circle Detection", output)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
