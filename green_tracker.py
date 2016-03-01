""" Program to track the motion of a green thing """

import cv2
import numpy as np
import time


cap = cv2.VideoCapture(0)

positions = []

while True:
    change = False

    # Capture frame-by-frame
    _, source = cap.read()
    #lowerBound = np.array([0,0,0])
    #upperBound = np.array([179,255,255])
    lowerBound = np.array([60, 64, 64])
    upperBound = np.array([70, 255, 255])

    frame = cv2.bilateralFilter(source, 9,75,75)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # convert to HSV
    frame = cv2.inRange(frame, lowerBound, upperBound)    # mask image
    contours,_ = cv2.findContours(frame, 1, 2)

    try:
        M = cv2.moments(contours[0])
    except IndexError:
        M = None
    try:
        cx = int(M['m10']/M['m00'])    # gets current position
        cy = int(M['m01']/M['m00'])
        positions.append((cx,cy))
    except ZeroDivisionError:
        cx = 0
        cy = 0
    except TypeError:
        cx = 0
        cy = 0

    frame = cv2.bitwise_and(source,source,mask= frame)        # recolor

    cv2.circle(frame, (cx,cy), 10, (0,255,0))    # circles the center of the contour

    for i in range(1,len(positions)):
        cv2.line(frame, positions[i-1],positions[i], (255,255,255))

    # Display the resulting frame
    cv2.imshow('Your Face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()