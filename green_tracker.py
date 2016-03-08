""" Program to track the motion of a green thing """

import cv2
import numpy as np
import time
import imutils



class Vector(object):   # a vector class for convinience
    def __init__(self,coords1,coords2):
        self.x = coords1[0]-coords2[0]
        self.y = coords1[1]-coords2[0]

    def __str__(self):
        return "<{},{}>".format(self.x,self.y)

    def __mul__(this,that):
        return this.x*that.x + this.y*that.y



cap = cv2.VideoCapture(0)

positions = [(0,0),(0,0),(0,0)]   # three previous positions
eventPosition = (0,0)   # position of last event
eventTime = time.time()

lowerBound = np.array([162, 150, 71])
upperBound = np.array([197, 205, 167])

while True:
    change = False

    # Capture frame-by-frame
    print cap.read()
    _, source = cap.read()

    #lowerBound = np.array([0,0,0])
    #upperBound = np.array([179,255,255])

    #frame = cv2.bilateralFilter(source, 9,75,75)
    source = imutils.resize(source, width=600)              # shrinks the image
    frame = cv2.GaussianBlur(source, (11, 11), 0)          # smooths the image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # convert to HSV
    frame = cv2.inRange(frame, lowerBound, upperBound)    # mask image
    frame = cv2.erode(frame, None, iterations=2)            # eliminates small fluccuations
    frame = cv2.dilate(frame, None, iterations=2)
    contours,_ = cv2.findContours(frame, 1, 2)

    try:
        M = cv2.moments(contours[0])
    except IndexError:
        M = None
    try:
        cx = int(M['m10']/M['m00'])    # gets current position
        cy = int(M['m01']/M['m00'])
        positions[2] = positions[1]
        positions[1] = positions[0]
        positions[0] = (cx,cy)
    except ZeroDivisionError:
        cx = 0
        cy = 0
    except TypeError:
        cx = 0
        cy = 0

    frame = cv2.bitwise_and(source,source,mask= frame)    # recolor

    cv2.circle(frame, (cx,cy), 10, (0,255,0))    # circles the center of the contour

    if Vector(positions[1],positions[2])*Vector(positions[0],positions[1]) < 0: # if a change in direction has occured
        eventPosition = positions[0]
        temp = eventTime
        eventTime = time.time()
        speed = 1000.0/(eventTime-temp)
        print speed
    cv2.circle(frame, eventPosition, 20, (0,0,255))

    # Display the resulting frame
    cv2.imshow('Your Face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()