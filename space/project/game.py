import pygame, sys
import random
from pygame.locals import *
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (800,600))


#Title an Icon 
pygame.display.set_caption("Space Invaders")
# icon = pygame.image.load('alien.png')
# pygame.display.set_icon(icon)
running = True
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (32,32))
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (64,64))
badguy1img = pygame.image.load('badguy1.png')
badguy1img = pygame.transform.scale(badguy1img, (80,80))

playerX = 370
playerY = 480

playerX_change = 0
   
#SOUND
# mixer.music.load('spaceinvaders1.mp3')
# mixer.music.play(-1)


 
#Badguy stuff
badguyImg = []
badguyX =[]
badguyY = []
badguyX_change =[]
badguyY_change = []
num_of_badguys = 6

for i in range(num_of_badguys):
    badguyImg.append(pygame.image.load('badguy1.png'))
    badguyX.append(random.randint(0,800))
    badguyY.append(random.randint (50,150))
    badguyX_change.append(4)
    badguyY_change.append(40)


# badguyX = random.randint(0,800)
# badguyY = random.randint(50,150)
# badguyX_change = 0.3
# badguyY_change = 40

#bullet
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


#SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY= 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text( ):
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))


def show_score(x,y):
    score = font.render("Score :" + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerImg, (x,y))
def badguy(x,y,i):
    screen.blit(badguy1img , (x,y ))   
    
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state ="fire"  
    screen.blit(bulletImg, (x + 16, y + 10))  
    
    
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX  - bulletX,2))+ math.pow(enemyY  -bulletY,2))
    if distance < 27:
        return True  
    else:
        return False
    
while running:
    screen.fill((0,0,0)) 
    
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #if keystroke is pressed check wheter is right or left
        if event.type  == pygame.KEYDOWN:
               
            if event.key == pygame.K_LEFT:
                 
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2       
            
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('shoot.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(playerX, bulletY)
    
                       
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
  
  #Check boundaries of spaceship so it stays in screen              
    playerX += playerX_change  
    
    if playerX <=0:
        playerX = 0
        badguyY +=badguyY_change
    elif playerX >= 736:
         playerX =736    
    
    
    #bullet movement
    if bulletY <=0:
        bulletY = 400
        bullet_state= "ready"
        
    if bullet_state == "fire":     
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change
    
    collision = isCollision(badguyX[i], badguyY[i], bulletX, bulletY)
    
    if collision:
        bulletY = 480
        explosion_sound = mixer.Sound('explosion2.wav')
        explosion_sound.play()
        bullet_state= "ready"
        score_value +=1 
        badguyX = random.randint(0, 800)
        badguyY= random.randint(50,150)
        
        
        
        
        
    #badguy movement  
    for i in range(num_of_badguys):
        # Game Over
        if badguyY[i]  >440:
            for j in range(num_of_badguys):
                badguyY[j] = 2000
            game_over_text()  
            break
           
        badguyX[i] += badguyX_change[i]
        
        if badguyX[i] <=0:
            badguyX_change[i] = 0.4
            badguyY[i] += badguyY_change[i]
        elif badguyX[i]>= 736:
            badguyX_change[i] =-0.4 
            badguyY[i] +=badguyY_change[i] 
            
        collision = isCollision(badguyX[i], badguyY[i], bulletX, bulletY)
    
        if collision:
            bulletY = 480     
            bullet_state= "ready"
            score_value +=1
              
            badguyX[i] = random.randint(0,736)
            badguyY[i]= random.randint(50,150)    
 
        show_score(textX, textY)    
        badguy(badguyX[i],badguyY[i],i)    
        show_score(textX, textY) 
        player(playerX,playerY)  
        
        pygame.display.update()    