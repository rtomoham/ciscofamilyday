# Implementation of classic arcade game Pong
# Debian code
# prerequisite: sudo apt-get install python-pygame

import pygame
import random
import time
from pygame.locals import *
from random import randint

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 50
NUMBER_OF_BALLS = 4
PAD_WIDTH = 8
PAD_HEIGHT = (80, 80)
MAX_V_SPEED = 1
MAX_H_SPEED = MAX_V_SPEED
# MIN_COORDINATES[0] == left gutter
# MIN_COORDINATES[1] == top of canvas
MIN_COORDINATES = (PAD_WIDTH, 0)
# MAX_COORDINATES[0] == right gutter
# MAX_COORDINATES[1] == bottom of canvas
MAX_COORDINATES = (WIDTH - PAD_WIDTH, HEIGHT)
PAD_LINE_THICKNESS = PAD_WIDTH
# define the colors we will use in the RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (136, 170, 207)
GREEN = (109, 221, 109)
RED =  (255, 105, 97)
YELLOW = (250, 250, 150)
BALL_COLOR = (BLUE, GREEN, YELLOW, RED)
BALLS = [1, 2, 3, 4]
PAD_COLOR = (BLUE, RED)
LEFT = False
RIGHT = True
PADDLE_SPEED = 2
TEXT_SIZE = 40

KEY1 = K_1
KEY2 = K_2
KEY3 = K_3
KEY4 = K_4
QUIT = K_ESCAPE

START_KEY = K_s

FONT_NAME = "monospace"
FONT_SIZE = 20

class Node:
    def __init__(self, number):
        self.number = number
        self.next = None
    
    def getNext(self):
        return self.next
        
    def getNumber(self):
        return self.number
        
    def setNext(self, node):
        self.next = node
    
class Ball:
    def __init__(self, number):
        self.number = number
        self.color = BALL_COLOR[number]
        
    def getColor(self):
        getColor = self.color
    
    def getNumber(self):
        getNumber = self.number

def keydown(key):
    if key == START_KEY:
        # user pushed start key
        # do nothing
        print "start key pushed"
    elif key == KEY1:
        return 1
    elif key == KEY2:
        return  2
    elif key == KEY3:
        return 3
    elif key == KEY4:
        return 4
    else:
        return -1
           
def keyup(key):
    if key == START_KEY:
        # user pushed start key
        # do nothing
        print "start key released"
    elif key == KEY1:
        keyup = 1
    elif key == KEY2:
        keyup = 2
    elif key == KEY3:
        keyup = 3
    elif key == KEY4:
        keyup = 4
    else:
        keyup = -1

def drawBall(nr):
    center = (WIDTH / 2, HEIGHT / 2)
#    pygame.draw.circle(screen, BALLS[ball].getColor(), center, BALL_RADIUS)
    pygame.draw.circle(screen, BALL_COLOR[nr-1], center, BALL_RADIUS)

    ballSurface = myfont.render(str(nr), 1, BLACK)
    screen.blit(ballSurface, (WIDTH / 2 - 5, HEIGHT / 2 - 10))

    pygame.display.flip()

#def getRandomBall():
#    ball = new Ball(randInt(0, NUMBER_OF_BALLS - 1)
#    getRandomBall = ball

def printMessage(message):
    messageSurface = myfont.render(message, 1, WHITE)
    screen.blit(messageSurface, (20, HEIGHT - 30))

    pygame.display.flip()
    
def generateSequence(length):
    i = 1
    nextNumber = randint(1, NUMBER_OF_BALLS)
    
    newNode = Node(nextNumber)
    startNode = newNode
    currentNode = startNode
    while i < length:
        nextNumber = randint(1, NUMBER_OF_BALLS)
        newNode = Node(nextNumber)
        currentNode.setNext(newNode)
        currentNode = newNode
        i += 1
    return startNode

def playSequence(node, delay):
    screen.fill(BLACK)
    time.sleep(delay/1000.0)
    drawBall(node.getNumber())
        
    time.sleep(delay/1000.0)
    screen.fill(BLACK)
    pygame.display.flip()
    
    nextNode = node.getNext()
    if not (nextNode is None):
        playSequence(nextNode, delay)
        
def playerInputCorrect(startNode):
    checking = True
    correct = True
    currentNode = startNode
    while checking:
        clock.tick(60)
        # Handle input events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                nr = keydown(event.key)
                print "key pressed: " + str(nr) + "\t\tnode number: " + str(currentNode.getNumber())
                if (currentNode.getNumber() == nr):
                    nextNode = currentNode.getNext()
                    if nextNode is None:
                        checking = False
                    else:
                        currentNode = currentNode.getNext()
                else:
                    correct = False
                    checking = False
            elif event.type == KEYUP:
                # ignore
                #keyup(event.key)
                break
    return correct    

# define event handlers
def newGame():
    running = True
    delay = 1000
    length = 1
    printMessage("*** Starting new game, get ready! ***")
    while running:
        startNode = generateSequence(length)

        screen.fill(BLACK)
        
        playSequence(startNode, delay)
        
        printMessage("Challenge length: " + str(length))
        
        if playerInputCorrect(startNode):
            screen.fill(BLACK)
            printMessage("You got the sequence of length " + str(length) + " correct!")
            length += 1
        else:
#            running = False
            screen.fill(BLACK)
            printMessage("You failed the sequence of length " + str(length) + ". Starting over...")
            length = 1

        screen.fill(BLACK)
        
# initialize the game engine
pygame.init()

# Set the height and width of the screen
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Simon Says")

clock = pygame.time.Clock()
myfont = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

BALLS[0] = Ball(0)
BALLS[1] = Ball(1)
BALLS[2] = Ball(2)
BALLS[3] = Ball(3)

#new_game()
running = True
while running:
    clock.tick(60)
    
    screen.fill(BLACK)

    running = newGame()
	

