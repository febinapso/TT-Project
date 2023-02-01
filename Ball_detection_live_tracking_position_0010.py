import cv2
import numpy as np

cap = cv2.VideoCapture(1)

refPt = []

def mouse_callback(event, x, y, flags, params):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]

cv2.namedWindow("frame")
cv2.setMouseCallback("frame", mouse_callback)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([20, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        else:
            center = (0, 0)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if refPt:
        x_coord = refPt[0][0] - x
        y_coord = refPt[0][1] - y
        print("Position coordinate of the orange ball with respect to the reference plane: ({}, {})".format(x_coord, y_coord))

cap.release()
cv2.destroyAllWindows()
