import threading
import time

# Piano Stairs V4 - > Very Basic PIN detection and sound Play with interruptions and threading!#Carles cferrate@cisco.com

#Import library for I/O pins
import RPi.GPIO as GPIO
#from EmulatorGUI import GPIO

#Import library for playing audio, init audio and load files
import pygame
pygame.mixer.init()

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

NUMBER_OF_INPUT_CHANNELS = 4
INPUT_CHANNEL = (18, 22, 24, 26)
PITCH = ("do", "re", "mi", "fa")
OUTPUT_CHANNEL = (12)
CHANNEL_IS_UP = (False, False, False, False)

DELAY = 0.05

def playSound(channel):
        for i in range (0, NUMBER_OF_INPUT_CHANNELS):
                if channel == INPUT_CHANNEL[i]:
                        sound = pygame.mixer.Sound(PITCH[i] + ".wav")
                        sound.play()
                        print(PITCH[i])

# set up the GPIO channels - one input and one output
for i in range(0, NUMBER_OF_INPUT_CHANNELS):
        # Setup pull_up_pull_down, we might not need this
        #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # or
        #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(INPUT_CHANNEL[i], GPIO.RISING)  # add rising edge detection on a channel
        GPIO.add_event_callback(INPUT_CHANNEL[i], playSound)
        
GPIO.setup(OUTPUT_CHANNEL[0], GPIO.OUT)
GPIO.output(OUTPUT_CHANNEL[0], GPIO.LOW)

# output to pin 12
GPIO.output(12, GPIO.LOW)
#GPIO.output(12, GPIO.HIGH)

def myEdgeUp(channel):
	if not CHANNEL_IS_UP[channel]:
		if 1 == GPIO.input(channel):
			try:
				thread.start_new_thread( playSound, channel)
				CHANNEL_IS_UP[channel] = True
			except:
			   print "Error: unable to start thread"
	elif:
		if 1 <> GPIO.input(channel):
			CHANNEL_IS_UP[channel] = False

while True:
	for i in range(0, NUMBER_OF_INPUT_CHANNELS):
		myEdgeUp(CHANNEL[i])
        # Sleep a bit, then check the pins again
        time.sleep(DELAY)
