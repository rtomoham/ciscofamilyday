import threading
import time

# Piano Stairs V4 - > Very Basic PIN detection and sound Play with interruptions and threading!#Carles cferrate@cisco.com

#Import library for I/O pins
import RPi.GPIO as GPIO
#from EmulatorGUI import GPIO
import time

#Import library for playing audio, init audio and load files
import pygame
pygame.mixer.init()
#do = pygame.mixer.Sound("do2.wav")
#re = pygame.mixer.Sound("re2.wav")
#mi = pygame.mixer.Sound("mi2.wav")
#fa = pygame.mixer.Sound("fa2.wav")

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up the GPIO channels - one input and one output
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(26, GPIO.LOW)

#Does it make sense to use Pull Up Pull DOwn???? 

GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(12, GPIO.OUT)

# output to pin 12
GPIO.output(12, GPIO.LOW)
#GPIO.output(12, GPIO.HIGH)

# input from pin 18
input_value = GPIO.input(18)
input_value2 = GPIO.input(22)
input_value3 = GPIO.input(24)
input_value4 = GPIO.input(26)

# Define a function per note -> Expect name( do, re mi, fa .. and INPUT pin)
def note( Name, pin):
#	print "%s is pin %s" % (Name, pin)
        print(Name + " is pin " + str(pin))
        sound = pygame.mixer.Sound(Name + ".wav")
        #sound.play()
        while True:
                #Filtering too fast signals!
                #GPIO.wait_for_edge(pin, GPIO.RISING)
                time_stamp = time.time()
                time_now = time_stamp
                while (time_now - time_stamp <0.0750) and (GPIO.input(pin)==1):
                        time_now = time.time()
                #time.sleep(0.01)
                if (GPIO.input(pin) == 1):
                        #GPIO.output(12, GPIO.HIGH)
                        sound.play()
                        print(Name)
                        GPIO.wait_for_edge(pin, GPIO.FALLING)
                        time.sleep(0.05)
                        
# Create threads per note and per sensor
try:
        thread.start_new_thread( note, ("do", 18, ) )
        thread.start_new_thread( note, ("re", 22, ) )
        thread.start_new_thread( note, ("mi", 24, ) )
        thread.start_new_thread( note, ("fa", 26, ) )

except:
        print("Error: unable to start thread")

while 1:
        pass
