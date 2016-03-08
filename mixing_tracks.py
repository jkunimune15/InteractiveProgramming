import pygame

import time

import math

pygame.init()

track1 = pygame.mixer.Sound("tws3.wav")
track2 = pygame.mixer.Sound("tws2.wav")
track3 = pygame.mixer.Sound("tws1.wav")
track4 = pygame.mixer.Sound("tws0.wav")

track1.play()
track2.play()
track3.play()
track4.play()

i = 0
while True:
	time.sleep(0.1)
	i = i+.1

	track1.set_volume(math.pow(math.sin(i),2))
	track2.set_volume(math.pow(math.sin(i/2.0),2))
	track3.set_volume(math.pow(math.sin(i/4.0),2))
	track4.set_volume(math.pow(math.sin(i/8.0),2))