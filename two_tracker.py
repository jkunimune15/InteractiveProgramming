""" Program to track the motion of a green thing and a red thing"""

import cv2
import numpy as np
import time
import imutils
import pygame

pygame.init()
#Now to play some music...
tracks = [pygame.mixer.Sound('tws0.wav'),pygame.mixer.Sound('tws1.wav'),pygame.mixer.Sound('tws2.wav'),pygame.mixer.Sound('tws3.wav')]

for track in tracks:
    track.set_volume(0.01)
    track.play()

screenWidth = 600
screenHeight = 450
columnWidth = screenWidth/4

class Frame(object):
    ''' Take in the video frame that the webcam sees and extract from it where the baton is.'''
    def __init__(self,color,position,vol=0.01):
        self.x = position[0]
        self.y = position[1]
        self.prevx = 240 #middle of screen
        self.prevy = 240

        self.color = color
        self.vol = vol
        
        self.filteredFrame = None
        self.y0 = None #y-value when the baton enters a column
        self.vol0 = None #vol value when the baton enters a column
        self.prevColumn = None
        self.Column = None

    def mask(self):
        '''Remove everything in-frame that isn't the color we want'''
        return cv2.inRange(self.filteredFrame, self.color.lowerBound, self.color.upperBound)    # mask image

    def track(self,filteredFrame):
        ''' Masks frame, updates old x and y positions, finds and updates new x and y positions'''
        self.filteredFrame = filteredFrame
        maskedframe = self.mask()
        contours,_ = cv2.findContours(maskedframe, 1, 2)
        M = cv2.moments(contours[0])

        # self.ppx, self.ppy = self.prevx, self.prevy #Reassign memory of old positions
        self.prevx, self.prevy = self.x, self.y

        cx = int(M['m10']/M['m00'])    # gets current position
        cy = int(M['m01']/M['m00'])

        self.x, self.y = cx, cy

    def volume_level(self):
        vol_step_upper = (1.0 - self.vol0) / float(self.y0)
        vol_step_lower = float(self.vol0) / (screenHeight - self.y0)

        if self.y < self.y0: #actually means it is HIGHER bc dumb coordinates
            self.vol += vol_step_upper * (self.y0 - self.y) #should be adding a positive quantity
        elif self.y > self.y0:
            self.vol += vol_step_lower * (self.y0 - self.y) #should be adding a negative quantity
        elif self.y == self.y0:
            self.vol = self.vol0
        
        return self.vol

    def volume_scale_change(self):
        '''Resets y0 and vol0, the reference points of what y and vol are when you enter a new zone.'''
        self.y0 = self.y
        self.vol0 = (450-self.y) / 450

    def whichColumn(self):
        ''' Specify a baton and this function returns which zone it's in: 0, 1, 2, or 3.'''
        if (self.x >= 0 and self.x < columnWidth):
            return 0

        elif (self.x >= columnWidth and self.x < 2*columnWidth):
            return 1

        elif (self.x >= 2*columnWidth and self.x < 3*columnWidth):
            return 2

        elif (self.x >= 3*columnWidth and self.x < screenWidth):
            return 3


class Color(object):
    '''Allows quick creation of a color in HSV'''
    def __init__(self, hue_min, hue_max = (hue_min + 23), sat_min=50, sat_max=255, vib_min=50, vib_max=255):
        self.hue_min = hue_min #hue
        self.hue_max = hue_max

        self.sat_min = sat_min #saturation
        self.sat_max = sat_max

        self.vib_min = vib_min #vibrance
        self.vib_max = vib_max
    def __str__(self):
        return "Green" #TODO: make this actually tell you what color it is

    def lowerBound(self):
        return np.array([hue_min,sat_min,vib_min])
    def upperBound(self):
        return np.array([hue_max,sat_max,vib_max])

limegreen = Color(60,80)
red = Color(1,25)

cap = cv2.VideoCapture(0)

green_baton = Frame(limegreen)
red_baton = Frame(red)

for baton in [green_baton, red_baton]:
    baton.prevColumn = baton.whichColumn()

while True:
    # Capture frame-by-frame
    print cap.read()
    _, source = cap.read()

    source = imutils.resize(source, width=600)              # shrinks the image
    frame = cv2.GaussianBlur(source, (11, 11), 0)          # smooths the image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # convert to HSV
    frame = cv2.erode(frame, None, iterations=2)            # eliminates small fluccuations
    frame = cv2.dilate(frame, None, iterations=2)

    green_baton.track(frame)
    red_baton.track(frame)

    frame = cv2.bitwise_and(source,source,mask= frame)    # recolor
    cv2.circle(frame, (green_baton.x,green_baton.y), 10, (0,255,0))    # circles the center of the contour
    cv2.circle(frame, (red_baton.x,red_baton.y), 10, (0,60,0)) #ELLIE NOTE: I changed the 255 to a 60 in that 3rd arg hoping it would be a different color

    # Display the resulting frame
    cv2.imshow('Your Face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    for baton in [green_baton,red_baton]:
        baton.Column = baton.whichColumn()

        #Has it changed to a new column?
            #If so, reset the relative y0 and vol0.
        if baton.Column != baton.prevColumn:
            baton.volume_scale_change()

        tracks[baton.Column].set_volume(baton.volume_level()) #Ok, now set the volume.

        
        #Reset "previous column"
        baton.prevColumn = baton.Column


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


'''THE GRAVEYARD LIES BELOW'''

    # try:
    #     M = cv2.moments(contours[0])
    # except IndexError:
    #     M = None
    # except ZeroDivisionError:
    #     cx = 0
    #     cy = 0
    # except TypeError:
    #     cx = 0
    #     cy = 0



# class Vector(object):   # a vector class for convenience
#     def __init__(self,coords1,coords2=[0,0]):
#         self.dx = coords1[0]-coords2[0]
#         self.dy = coords1[1]-coords2[0]

#     def __str__(self):
#         return "<{},{}>".format(self.dx,self.dy)

#     def __mul__(this,that):
#         return (this.dx*that.dx , this.dy*that.dy)


    # def is_changedir(self):
    #     ''' Determines if the baton being tracked has changed direction '''
    #     old_dx = self.prevx - self.ppx
    #     new_dx = self.x - self.prevx
    #     old_dy = self.prevy - self.ppx
    #     new_dy = self.y - self.prevy
    #     #If either of the product of old/new dx or dy is negative (aka if either pair has different signs)
    #     if (old_dx*new_dx<0 or old_dy*new_dy<0):
    #         return True
    #     else:
    #         return False