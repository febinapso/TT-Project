import cv2
import numpy as np

# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(1)

# Initialize the previous center of the orange ball
prev_center = None

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for the orange color in HSV space
    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([20, 255, 255])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Perform morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If a contour is found, draw a circle around the orange ball
    center = None
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) < 100:
            continue
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        color = (0, 255, 0)
        thickness = 2
        cv2.circle(frame, center, radius, color, thickness)

    # If the previous center of the orange ball was found,
    # draw a line from the previous center to the current center
    if prev_center is not None and center is not None:
        color = (0, 0, 255)
        thickness = 2
        cv2.line(frame, prev_center, center, color, thickness)

    # Update the previous center of the orange ball
    if center is not None:
        prev_center = center

    # Display the output
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
