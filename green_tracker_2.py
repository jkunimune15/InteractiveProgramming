""" Program to track the motion of a green thing.
Ellie fuckin around mode: measures green thing's vertical distance from center,
uses that to control volume of music. """

import cv2
import numpy as np
import time
import pygame
import imutils



#lowerBound = np.array([0,0,0])         #Everything
#upperBound = np.array([179,255,255])
#lowerBound = np.array([160, 64, 64])   #Magenta
#upperBound = np.array([169, 255, 255])
#lowerBound = np.array([25,120,120])       #Chartreuse
#upperBound = np.array([30,255,255])
lowerBound = np.array([162, 150, 71])   #Red
upperBound = np.array([197, 205, 167])



def volAdjust(c_y):
    ''' Input y coordinate (measured pos down from top of screen) cy
    Outputs a volume scaled from 0 to 1 - higher is louder, lower is quiet
    Coordinate system: 0 (top) to 480 (bottom)
    Output coord system: 1 (top) to 0 (bottom)'''
    c_y = -1.0 * c_y
    vol = (float(c_y)/480) + 1.0
    return vol


pygame.init()
#Now to play some music...
m = pygame.mixer.music.load('music.wav')
pygame.mixer.init(1100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.01)

cap = cv2.VideoCapture(0)

positions = []

while True:
    change = False

    # Capture frame-by-frame
    _, source = cap.read()

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
        positions.append((cx,cy))
        if pygame.mixer.music.get_busy() == True:
            Vol = volAdjust(cy)
            pygame.mixer.music.set_volume(Vol)
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
