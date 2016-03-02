'''Playing with pygame's sound/music/mixer modules
EFunkhouser 2/29/2016'''
import pygame
import wave #test this out in series & in parallel w/mixer...but must be on .wav files
pygame.init()

# import os
# os.getcwd() # Log this line.
# soundObj = pygame.mixer.Sound('airplaneWav.wav')

m = pygame.mixer.music.load('testSong.ogg')
pygame.mixer.init(1100, 16, 2, 4096) #frequency, size, channels, buffersize
# pygame.mixer.music.load('airplaneWav.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.01)
while pygame.mixer.music.get_busy() == True:
	bigVol = raw_input("Please enter a volume between 0 and 100:")
	Vol = float(bigVol) / 100.0
	print pygame.mixer.music.get_volume()
	pygame.mixer.music.set_volume(Vol)
	print pygame.mixer.music.get_volume()