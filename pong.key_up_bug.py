# Implementation of classic arcade game Pong
# Debian code
# prerequisite: sudo apt-get install python-pygame

import pygame
import random
from pygame.locals import *

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
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
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (136,170,207)
GREEN = (109,221,109)
RED =  (255,105,97)
BALL_COLOR = GREEN
PAD_COLOR = (BLUE, RED)
LEFT = False
RIGHT = True
PADDLE_SPEED = 2
TEXT_SIZE = 40

P1UP = K_w
P1DOWN = K_s
P2UP = K_UP
P2DOWN = K_DOWN
QUIT = K_ESCAPE

FONT_NAME = "monospace"
FONT_SIZE = 28

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]

    vertical_velocity = random.randrange(-3, -1)
    horizontal_velocity = random.randrange(2, 4)
    if direction == LEFT:
        horizontal_velocity = -horizontal_velocity
    ball_vel = [horizontal_velocity, vertical_velocity]

def increase_ball_speed():
    # increases the ball velocity in both the horizontal and vertical direction
    # with 10%
    ball_vel[0] = 1.1 * ball_vel[0]
    ball_vel[1] = 1.1 * ball_vel[1]
    
def update_ball():
    # helper function to update the ball position and velocity
    # i == 0 -> update horizontal position
    # i == 1 -> update vertical position
    global score1, score2;
    global ball_vel
    
    for i in range(0, 2):
        # i == 0 -> make horizontal adjustment
        # i == 1 -> make vertical adjustment
        ball_pos[i] += ball_vel[i]
        if (ball_pos[i] <= MIN_COORDINATES[i] + BALL_RADIUS):
            # ball reached either a side or top or bottom
            # i == 0 -> ball reached the left gutter/paddle
            # i == 1 -> ball reached the top
            ball_pos[i] = (MIN_COORDINATES[i] + BALL_RADIUS) + (MIN_COORDINATES[i] + BALL_RADIUS - ball_pos[i])
            ball_vel[i] = -ball_vel[i]
            if i == 0:
                # ball reached the left gutter, now check if it hits the left paddle
                if not ((ball_pos[1] >= paddles_top[0]) and (ball_pos[1] <= paddles_top[0] + PAD_HEIGHT[0])):
                    # nope, so grant right player a point and respawn
                    score2 += 1
                    spawn_ball(RIGHT)
                else:
                    # ball hit a paddle, so increase the speed by 10%
                    increase_ball_speed()
        elif (ball_pos[i] >= MAX_COORDINATES[i] - BALL_RADIUS):
            # ball reached either a side or top or bottom
            # i == 0 -> ball reached the right gutter/paddle
            # i == 1 -> ball reached the bottom
            ball_pos[i] = (MAX_COORDINATES[i] - BALL_RADIUS) - (ball_pos[i] - (MAX_COORDINATES[i] - BALL_RADIUS))
            ball_vel[i] = -ball_vel[i]
            if i == 0:
                # ball reached the right gutter, now check if it hits the right paddle
                if not ((ball_pos[1] >= paddles_top[1]) and (ball_pos[1] <= paddles_top[1] + PAD_HEIGHT[1])):
                    # nope, so grant left player a point and respawn
                    score1 += 1
                    spawn_ball(LEFT)                    
                else:
                    # ball hit a paddle, so increase the speed by 10%
                    increase_ball_speed()

def update_paddles():
    # updates the position of the paddles
    # paddles_top[0] == y coordinate of the top of the left paddle
    # paddles_top[1] == y coordinate of the top of the right paddle 
    for i in range(0, 2):
        paddles_top[i] += paddles_vel[i]
        if paddles_top[i] < 0:
            paddles_top[i] = MIN_COORDINATES[1]
            paddles_vel[i] = 0
        elif paddles_top[i] + PAD_HEIGHT[i] > HEIGHT:
            paddles_top[i] = HEIGHT - PAD_HEIGHT[i]
            paddles_vel[i] = 0

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global paddles_top # I prefer to use the tops of the paddles in a list
    global score1, score2  # these are ints

    paddles_top = [HEIGHT / 2 - PAD_HEIGHT[0] / 2, HEIGHT / 2 - PAD_HEIGHT[1] / 2]
    
    score1 = 0
    score2 = 0
    
    spawn_ball(RIGHT)

def draw():
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global screen
        
    # draw mid line and gutters
    pygame.draw.line(screen, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(screen, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(screen, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
        
    # update paddle's vertical position, keep paddle on the screen
    update_paddles()
    
    # update ball
    update_ball()
    
    # draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # draw paddles
    pad_left = [0, WIDTH - PAD_WIDTH]
    for i in range(0, 2):
        pygame.draw.rect(screen, PAD_COLOR[i], [pad_left[i], paddles_top[i], PAD_WIDTH, PAD_HEIGHT[i]])
   
    # draw scores
    score1_surface = myfont.render(str(score1), 1, WHITE)
    score2_surface = myfont.render(str(score2), 1, WHITE)
    if (score1 < 10):
        screen.blit(score1_surface, (WIDTH / 2 - 60, 40))
    else:
        screen.blit(score1_surface, (WIDTH / 2 - 80, 40))

    screen.blit(score2_surface, (WIDTH / 2 + 40, 40))
        
    pygame.display.flip()
        
def keydown(key):
    # w == left pad up
    # s == left pad down
    # arrow_up == right pad up
    # arrow_down == right pad down
    # w & s and the same time == left pad stop
    # arrow_up and down at the same time == right pad stop        
    
    global left_paddle_up, left_paddle_down, right_paddle_up, right_paddle_down

    if key == P1UP:
        # user pushed up key for left paddle
        left_paddle_up = True
        if paddles_vel[0] == 0:
            # up is the only command for the left paddle, so move it up 
            paddles_vel[0] = -PADDLE_SPEED
        else:
            # user is also pushing the down key for the left paddle, so freeze
            paddles_vel[0] = 0
    elif key == P1DOWN:
        # user pushed down key for left paddle
        left_paddle_down = True
        if paddles_vel[0] == 0:
            # down is the only command for the left paddle, so move it down 
            paddles_vel[0] = PADDLE_SPEED
        else:
            # user is also pushing the up key for the left paddle, so freeze
            paddles_vel[0] = 0
    elif key == P2UP:
        # user pushed up key for right paddle
        right_paddle_up = True
        if paddles_vel[1] == 0:
            # up is the only command for the right paddle, so move it up 
            paddles_vel[1] = -PADDLE_SPEED
        else:
            # user is also pushing the down key for the right paddle, so freeze
            paddles_vel[1] = 0
    elif key == P2DOWN:
        # user pushed down key for right paddle
        right_paddle_down = True
        if paddles_vel[1] == 0:
            # down is the only command for the right paddle, so move it down 
            paddles_vel[1] = PADDLE_SPEED
        else:
            # user is also pushing the up key for the right paddle, so freeze
            paddles_vel[1] = 0
   
def keyup(key):
    # w == left pad up
    # s == left pad down
    # arrow_up == right pad up
    # arrow_down == right pad down
    # if for a given paddle both up and down were pressed, and the users
    # releases one of them, then the paddle should move in the direction
    # of the remaining button that's pressed down

    global left_paddle_up, left_paddle_down, right_paddle_up, right_paddle_down
    global running

    if key == P1UP:
        # user released the up key for the left paddle
        left_paddle_up = False
        if left_paddle_down == True:
            # user is still pushing the down key for the left paddle
            paddles_vel[0] = PADDLE_SPEED
        else:
            # user is not pushing any keys for the left paddle
            paddles_vel[0] = 0
    elif key == P1DOWN:
        # user released the down key for the left paddle
        left_paddle_down = False
        if left_paddle_up == True:
            # user is still pushing the up key for the left paddle
            paddles_vel[0] = -PADDLE_SPEED
        else:
            # user is not pushing any keys for the left paddle
            paddles_vel[0] = 0
    elif key == P2UP:
        # user released the up key for the right paddle
        right_paddle_up = False
        if right_paddle_down == True:
            # user is still pushing the down key for the right paddle
            paddles_vel[1] = PADDLE_SPEED
        else:
            # user is not pushing any keys for the right paddle
            paddles_vel[1] = 0
    elif key == P2DOWN:
        # user released the down key for the right paddle
        right_paddle_down = False
        if right_paddle_up == True:
            # user is still pushing the up key for the right paddle
            paddles_vel[1] = -PADDLE_SPEED
        else:
            # user is not pushing any keys for the right paddle
            paddles_vel[1] = 0
    elif key == QUIT:
        running = False

# initialize the game engine
pygame.init()

# Set the height and width of the screen
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pong")

#frame.set_keydown_handler(keydown)
#frame.set_keyup_handler(keyup)
#frame.add_button("Restart game", new_game, 200)

# initialize paddle states
def init_paddle_states():
    # this needs only be done once, in case the user is pushing any (or multiple)
    # paddle keys when (s)he restarts the game
    global left_paddle_up, left_paddle_down, right_paddle_up, right_paddle_down
    global paddles_vel # I prefer to use the vel of the paddles in a list

    left_paddle_up = False
    left_paddle_down = False
    right_paddle_up = False
    right_paddle_down = False

    paddles_vel = [0, 0]

    

clock = pygame.time.Clock()
init_paddle_states()
myfont = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# start frame
new_game()
#frame.start()
draw()
running = True
while running:
    clock.tick(60)
    
    screen.fill(BLACK)
    draw()
	
    # Handle input events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            keydown(event.key)
            break
        elif event.type == KEYUP:
            keyup(event.key)
            break

