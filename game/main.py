import pygame
import random
import math
from pygame import mixer

pygame.init()

#setting up screen
screen = pygame.display.set_mode((800, 600))

#Icon and Title
pygame.display.set_caption('Monkey See Monkey Do')
icon = pygame.image.load('Images\Icon.png')
pygame.display.set_icon(icon)

#Background Image
background_img = pygame.image.load('Images\Background.jpg')

#Background sound
mixer.music.load("Sound\Background.mp3")
mixer.music.play(-1)


textX = 10
textY = 10

#Font of Score
font = pygame.font.Font('freesansbold.ttf', 32)
score_value = 0

#Font of Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#Player
playerImg = pygame.image.load('Images\player.png')
playerX = 370
playerY = 480
playerX_change = 0

#BANANA
bananaImg = pygame.image.load('Images\Banana.png')
bananaX = 0
bananaY = 480
bananaX_change = 0
bananaY_change = 18
banana_state = 'ready'        #Not fired

#Enemy
enemies = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_num = 10

for i in range(enemy_num):
    enemies.append(pygame.image.load('Images\enemy2.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(50)
    enemyY_change.append(10)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))


def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200,250))
    over2 = over_font.render("SCORE: " + str(score_value), True, (0, 255, 0))
    screen.blit(over2, (235, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemies[i], (x,y))

def banana_throw(x, y):
    global banana_state
    banana_state = 'fire'
    screen.blit(bananaImg, (x+10, y+10))

def collision(enemyX, enemyY, bananaX, bananaY):
    dist = math.sqrt((enemyX-bananaX)**2 +(enemyY - bananaY)**2)
    if dist < 27:
        return True
    else:
        return False

running = True

while running:

    screen.blit(background_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if banana_state is 'ready':
                    monkeySound = mixer.Sound("Sound\chimpanzee.wav")
                    monkeySound.play()
                    bananaX = playerX
                    banana_throw(bananaX, bananaY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(enemy_num):

        if enemyY[i] > 440:
            for j in range(enemy_num):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            # enemyX_change[i] = 2
            #
            if score_value> 20:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i] + 10
            elif score_value> 40:
                enemyX_change[i] = 10
                enemyY[i] += enemyY_change[i] + 20
            else:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            #enemyX_change[i] = -2
            if score_value> 20:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i] + 10
            elif score_value> 40:
                enemyX_change[i] = -10
                enemyY[i] += enemyY_change[i] + 20
            else:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

        collide = collision(enemyX[i], enemyY[i], bananaX, bananaY)
        if collide:
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            bananaY = 480
            banana_state = 'ready'
            score_value += 1



        enemy(enemyX[i], enemyY[i], i)



    if bananaY <= -75:
        bananaY = 480
        banana_state = 'ready'

    if banana_state is 'fire':
        banana_throw(bananaX, bananaY)
        bananaY -= bananaY_change


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()