import pygame

import time

import math

pygame.init()

pygame.mixer.init(22100)

pygame.mixer.music.load("music.wav")

pygame.mixer.music.play()

i = 0
while True:
	time.sleep(0.1)
	i = i+.1
	pygame.mixer.music.set_volume(math.pow(math.sin(i),2))