import os, sys, wave, pygame, numpy, pymedia.audio.sound, scikits.samplerate

class Window:
    def __init__(self, width, height, minOctave, maxOctave):
        """
        width, height: the width and height of the screen.
        minOctave, maxOctave: the highest and lowest pitch changes. 0 is no change.
        """
        self.minOctave = minOctave
        self.maxOctave = maxOctave
        self.width = width
        self.mouseDown = False
        self.ratio = 1.0 # The resampling ratio
        waveRead = wave.open(os.path.join(sys.path[0], "music.wav"), 'rb')
        sampleRate = waveRead.getframerate()
        channels = waveRead.getnchannels()
        soundFormat = pymedia.audio.sound.AFMT_S16_LE
        soundOutput = pymedia.audio.sound.Output(sampleRate, channels, soundFormat)
        pygame.init()
        screen = pygame.display.set_mode((width, height), 0)
        screen.fill((255, 255, 255))
        pygame.display.flip()
        fout = open(os.path.join(sys.path[0], "musicdata.txt"), 'w') # For troubleshooting
        byteString = waveRead.readframes(1000) # Read at most 1000 samples from the file.
        while len(byteString) != 0:
            self.handleEvent(pygame.event.poll()) # This does not wait for an event.
            fout.write(str(soundOutput.getLeft()) + "\n") # For troubleshooting
            if soundOutput.getLeft() < 0.2: # If there is less than 0.2 seconds left in the sound buffer.
                array = numpy.fromstring(byteString, dtype=numpy.int16)
                byteString = scikits.samplerate.resample(array, self.ratio, "sinc_fastest").astype(numpy.int16).tostring()
                soundOutput.play(byteString)
                byteString = waveRead.readframes(500) # Read at most 500 samples from the file.
        waveRead.close()
        return

    def handleEvent(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouseDown = True
            self.setRatio(event.pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouseDown = False
        if event.type == pygame.MOUSEMOTION and self.mouseDown:
            self.setRatio(event.pos)
        return None

    def setRatio(self, point):
        self.ratio = 2 ** -(self.minOctave + point[0] * (self.maxOctave - self.minOctave) / float(self.width))
        print(self.ratio)

def main():
    Window(768, 100, -2.0, 2.0)

if __name__ == '__main__':
    main()