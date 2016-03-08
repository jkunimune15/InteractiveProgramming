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
lowerBound = np.array([153, 100, 67])   #Magenta
upperBound = np.array([191, 197, 223])
#lowerBound = np.array([25,120,120])       #Chartreuse
#upperBound = np.array([30,255,255])
#lowerBound = np.array([162, 150, 71])   #Red
#upperBound = np.array([197, 205, 167])

screenWidth = 600
screemHeight = 450
columnWidth = screenWidth/4



def volAdjust(c_y):
    ''' Input y coordinate (measured pos down from top of screen) cy
    Outputs a volume scaled from 0 to 1 - higher is louder, lower is quiet
    Coordinate system: 0 (top) to 480 (bottom)
    Output coord system: 1 (top) to 0 (bottom)'''
    c_y = -1.0 * c_y
    vol = (float(c_y)/screenWidth) + 1.0
    return vol


pygame.init()
#Now to play some music...
tracks = [pygame.mixer.Sound('tws0.wav'),pygame.mixer.Sound('tws1.wav'),pygame.mixer.Sound('tws2.wav'),pygame.mixer.Sound('tws3.wav')]
for track in tracks:
    track.set_volume(.5)
    track.play()

cap = cv2.VideoCapture(0)

positions = []
cx = 0
cy = 0

while True:
    change = False

    # Capture frame-by-frame
    _, source = cap.read()

    source = imutils.resize(source, width=600)              # shrinks the image
    source = cv2.flip(source,1)                             # flips image
    frame = cv2.GaussianBlur(source, (11, 11), 0)          # smooths the image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # convert to HSV
    frame = cv2.inRange(frame, lowerBound, upperBound)    # mask image
    frame = cv2.erode(frame, None, iterations=2)            # eliminates small fluccuations
    frame = cv2.dilate(frame, None, iterations=2)
    contours,_ = cv2.findContours(frame, 1, 2)
    frame = cv2.bitwise_and(source,source,mask= frame)        # recolor

    try:
        M = cv2.moments(contours[0])
    except IndexError:
        print (cx,cy)
        continue
    cx = int(M['m10']/M['m00'])    # gets current position
    cy = int(M['m01']/M['m00'])
    Vol = volAdjust(cy)
    if cx < columnWidth:
        tracks[3].set_volume(Vol)                    # adjusts the appropriate track volume
        cv2.circle(frame, (cx,cy), 30, (0,0,255), thickness=5)
    elif cx < columnWidth*2:
        tracks[2].set_volume(Vol)
        cv2.circle(frame, (cx,cy), 30, (0,200,200), thickness=5)
    elif cx < columnWidth*3:
        tracks[1].set_volume(Vol)
        cv2.circle(frame, (cx,cy), 30, (0,255,0), thickness=5)
    else:
        tracks[0].set_volume(Vol)
        cv2.circle(frame, (cx,cy), 30, (255,0,0), thickness=5)

    # Display the resulting frame
    cv2.imshow('Your Face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
