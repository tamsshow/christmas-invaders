import pygame
import random
import math
from pygame import mixer
from time import sleep

#initializing pygame
pygame.init()

#creating da window
screen = pygame.display.set_mode((800,600))

#title and icon and timer
pygame.display.set_caption("Christmas Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

#background
background = pygame.image.load("background.png")

#background sound
def background_music():
    mixer.music.load("thomas the tank engine earrape.wav")
    mixer.music.set_volume(0.05)
    mixer.music.play(-1)

#font
large_text = pygame.font.Font("freesansbold.ttf", 100)
regular_text = pygame.font.Font("freesansbold.ttf", 16)

#color
white = (255,255,255)
black = (0,0,0)
green = (0,200,0)
red = (200,0,0)
light_red = (255,0,0)
light_green = (0,255,0)

#left click
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()
left_click = click[0]

def control_screen():

    screen.fill(white)

    left = regular_text.render("Press A or Left Arrow Key to go Left", True, black)
    right = regular_text.render("Press D or Right Arrow Key to go Right", True, black)
    shoot = regular_text.render("Press W or Up Arrow Key to Shoot", True, black)
    exit = regular_text.render("Press Space to Continue", True, black)
    quit_msg = regular_text.render("Press Q to Quit", True, black)
    screen.blit(left, (80, 200))
    screen.blit(right, (80, 240))
    screen.blit(shoot, (80, 280))
    screen.blit(exit, (5, 580))
    screen.blit(quit_msg, (80, 320))

    clock.tick(15)
    pygame.display.update()



def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        intro_text1 = large_text.render("CHRISTMAS", True, black)
        intro_text2 = large_text.render("INVADERS", True, black)
        desc = regular_text.render("Basically bootleg Galaga", True, black)
        screen.blit(intro_text1, (80, 150))
        screen.blit(intro_text2, (80, 260))
        screen.blit (desc, (80,360))

        #getting mouse position and clicks
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        left_click = click[0]

        #creating two buttons for controls and start
        if 150+100 > mouse[0] > 150 and 400+50 > mouse [1] > 400:
            button(150,400,50,100, light_green, "Continue", black)
            if left_click == 1:
                state = "playing"
                return state
        else:
            button(150,400,50,100, green, "Continue", black)

        if 550 + 100 > mouse[0] > 550 and 400 + 50 > mouse [1] > 400:
            button(550, 400, 50, 100, light_red, "Controls", black)
            if left_click == 1:
                state = "controls"
                return state
        else:
            button(550, 400, 50, 100, red, "Controls", black)


        pygame.display.update()


def button(button_x, button_y, button_height, button_width, button_color, button_text, button_text_color):

    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    button_text = regular_text.render(button_text, True, black)
    screen.blit(button_text, (button_x + (button_width/8), button_y + (button_height/3)))


class Player():
    #the player
    def __init__(self):
        self.x = 370.0
        self.y = 480.0
        self.image = pygame.image.load("player.png")
        self.xchange = 0
        self.xbound_right = 736
        self.xbound_left = 0
    def draw(self):
        self.x += self.xchange
        if self.in_bounds() == True:
            screen.blit(self.image, (self.x, self.y))
        else:
            if self.x >= self.xbound_right:
                self.x = self.xbound_right
                screen.blit(self.image, (self.x, self.y))
            elif self.x <= self.xbound_left:
                self.x = self.xbound_left
                screen.blit(self.image, (self.x, self.y))
    def move(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.xchange = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.xchange = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_d:
                self.xchange = 0
    def in_bounds(self):
        if self.x <= self.xbound_right and self.x >= self.xbound_left:
            return True
        else:
            return False

class Enemy():
    def __init__(self):
        self.image = pygame.image.load("enemy.png")
        self.xchange = 5
        self.ychange = 20
        self.xbound_right = 735
        self.xbound_left = 0
        self.ybound_up = 50
        self.ybound_down = 100
        self.x = random.randint(self.xbound_left, self.xbound_right)
        self.y = random.randint (self.ybound_up,self.ybound_down)
        self.moving = True
    def draw(self):
        self.x += self.xchange
        screen.blit(self.image, (self.x, self.y))
    def in_bounds(self):
        if self.x <= self.xbound_right and self.x >= self.xbound_left:
            return True
        else:
            return False
    def move(self):
        self.x += self.xchange
        if self.x <= self.xbound_left:
            self.xchange = 5
            self.y += self.ychange
        elif self.x >= self.xbound_right:
            self.xchange = -5
            self.y += self.ychange
    def reset(self):
        self.x = random.randint(self.xbound_left, self.xbound_right)
        self.y = random.randint (self.ybound_up,self.ybound_down)

class Bullet():
    def __init__(self):
        self.x = 0
        self.y = 480
        self.ychange = 20
        #ready = cant see bullet; fire = bullet moving
        self.state = "ready"
        self.image = pygame.image.load("bullet.png")
    def draw(self,playerx):
        #initializes the bullet basically
        self.state = "fire"
        screen.blit(self.image, (playerx + 16, self.y + 10))
    def fire(self,playerx):
        #check if w or up key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                #makes sure it is only drawn the fist time/ not redrawn every time w/up is pressed
                if self.state == "ready":
                    bullet_sound = mixer.Sound("pew.wav")
                    bullet_sound.play()
                    self.x = playerx
                    self.draw(self.x)
    def move(self):
        #resets bullet once it goes off screen
        if self.y <= 0:
            self.y = 480
            self.state = "ready"
        #moves bullet once fired
        if self.state is "fire":
            self.draw(self.x)
            self.y -= self.ychange

def isCollision(enemyX,enemyY,bulletX,bulletY):
    #using distance formula to find distance between bullet and enemy
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    #if the ditance is less than 27 pixels
    if distance < 48:
        return True
    else:
        return False


spaceship = Player()
number_of_enemies = 3
enemies = [Enemy() for i in range (number_of_enemies)]

bullet = Bullet()

#score
class Score():
    def __init__(self):
        self.x = 10
        self.y = 10
        self.value = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
    def show_score(self):
        score = self.font.render("Score: %i" %(self.value), True, white)
        screen.blit(score, (self.x,self.y))
    def increase(self):
        self.value += 1
score_value = Score()

#game over sequence
def game_over():
    over_text = large_text.render("GAME OVER", True, white)
    screen.blit(over_text, (80, 200))

#game intro
state = game_intro()

#start ticks for countdown
start_ticks = pygame.time.get_ticks()

#countdown timer
class Timer():
    def __init__(self,start):
        self.endtime = 30
        self.x = 650
        self.y = 10
        self.start_tick = start
        self.seconds = 0
        self.pause_time = 0
    def display(self,state):
        game_start = pygame.time.get_ticks()
        if state == "controls" or state == "pause":
            self.pause_time = pygame.time.get_ticks() / 1000
            print (self.pause_time)
        self.seconds = ((game_start - self.start_tick) / 1000)  # calculate how many seconds
        timer_display = self.endtime - self.seconds + self.pause_time
        timer_text = regular_text.render("Time Left: %is" % (timer_display), True, white)
        if state == "playing":
            screen.blit(timer_text, (650, 10))

        #if time is up
        if timer_display <= 0:
            state = "game over"
            return state
        else:
            return state






    #clock.tick(30)
    #pygame.display.update()

#game loop
running = True

# background music
background_music()

while running:
    #drawing the screen color (r,g,b)
    screen.fill(black)
    #backgound image
    screen.blit(background, (0,0))


    #getting every event in console
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = "playing"
            if event.key == pygame.K_c:
                state = "controls"
            if event.key == pygame.K_p:
                state = "pause"
            if event.key == pygame.K_q:
                running = False


        if state == 'playing':
            spaceship.move()
            bullet.fire(spaceship.x)

    if state == "playing":
        mixer.music.unpause()
        timer = Timer(start_ticks)
        state = timer.display(state)

        spaceship.draw()

        #creating all enemies
        for i in range(number_of_enemies):
            enemies[i].draw()
            enemies[i].move()

            # collision detecting
            collision = isCollision(enemies[i].x, enemies[i].y, bullet.x, bullet.y)
            if collision == True:
                hit_sound = mixer.Sound("nani.wav")
                hit_sound.play()
                bullet.y = 480
                bullet.state = "ready"
                score_value.increase()
                enemies[i].reset()
            #game over
            if enemies[i].y >= 400:
                for j in range(number_of_enemies):
                    enemies[j].y = 2000
                game_over()
                break


        bullet.move()
        score_value.show_score()

    elif state == "controls":
        screen.fill(black)
        state = timer.display(state)
        mixer.music.pause()
        control_screen()
        sleep(30)
        state = 'playing'

    elif state == "pause":
        mixer.music.pause()
        state = timer.display(state)
        pause_text = large_text.render("PAUSE", True, white)
        continue_msg = regular_text.render("Press Space to Continue", True, white)
        quit_msg = regular_text.render("Press Q to Quit", True, white)
        screen.blit(pause_text, (225, 200))
        screen.blit(continue_msg, (225, 305))
        screen.blit(quit_msg, (225, 325))

    elif state == 'game over':
        mixer.music.stop()
        game_over()
        score_value.show_score()



    pygame.display.update()

