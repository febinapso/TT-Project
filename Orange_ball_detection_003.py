import cv2
import numpy as np

# Read the input image
img = cv2.imread('input2.jpeg')

# Convert to the HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

# Draw a circle around each orange ball
for contour in contours:
    if cv2.contourArea(contour) < 100:
        continue
    (x, y), radius = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    radius = int(radius)
    color = (0, 255, 0)
    thickness = 2
    cv2.circle(img, center, radius, color, thickness)

# Display the output
cv2.imshow('img', img)
cv2.waitKey()
