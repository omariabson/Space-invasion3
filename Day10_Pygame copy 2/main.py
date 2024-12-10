# MAIN
# do the preparation of installing pygame first
#

import pygame
import random  # for enemy movement
import math    # to do math formulas
from pygame import mixer  # to work with sounds

# INITIALIZE GAME <<<<<<<<<<<<<<<<<<<<<
pygame.init()  # run pygame to get access to its tools

# MAKE_SCREEN_2 <<<<<<<<<<<<<<<<<<<<<<<<
screen = pygame.display.set_mode((800, 600))  # resolution: H = 800px W = 600px
# - note: we need to make a live Quit event in GameLoop for it to stay open

pygame.display.set_caption("Space Invasion")  # title shows at top of screen

# make icon... !!!Mac Sequoia doesn't do icons now!!!!
# icon = pygame.image.load("ufo.png")  # icon must be 32x32
# pygame.display.set_icon(icon)  # now can call it in Game loop

background = pygame.image.load('space_background.jpg')  # make sure BGrd image same dimensions as screen
# background = pygame.image.load('DNC_Background.png')  # make sure BGrd image same dimensions as screen

# SOUND FX <<<<<<<<<<<<<<<<<<<
# background music...
mixer.music.load('Planet Rock.mp3')
mixer.music.set_volume(0.3)  # set volume
mixer.music.play(-1)  # -1 makes the music loop

# PLAYER MOCK CLASS <<<<<<<<<<<<<<<<<<<<<<<
# player variables...
# img_player = pygame.image.load("sniper_dark.jpg")  # use a 64x64px img
img_player = pygame.image.load("rocket.png")  # use a 64x64px img
player_x = 368  # to initially place rocket in middle: (800/2) - (rocket width/2)
player_y = 500  # to initially place at bottom: 600 - rocket height
player_x_change = 0  # initial lateral speed/movement (will be user controlled)


# player function...
def player(x, y):
    # screen.blit(img_player, (player_x, player_y))  
    # - now call this function in the game loop before the update code line

    # MOVE THE PLAYER_5 <<<<<<<<<<<<<<<<<<<<<<<<
    screen.blit(img_player, (x, y))  # soft-code the above code line
    # - now in the Game Loop we can code it to control its movement


# ENEMY MOCK CLASS <<<<<<<<<<<<<<<<<<<<<<<<<<<
# note: the computer will randomly place the enemy then control its movement
# enemy variables...
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy = pygame.image.load("enemy_explosion_img.png")
number_of_enemies = 8

# create multiple enemies...
for e in range(number_of_enemies):
    # img_enemy.append(pygame.image.load("Enemy.png"))  # 64x64px
    img_enemy.append(pygame.image.load('enemy.png'))  # 64x64px
    enemy_x.append(random.randint(0, 736))  # random position x
    enemy_y.append(random.randint(50, 200))  # random position y
    enemy_x_change.append(0.2)  # when reaches side of screen will move  0.3px/iteration to the right
    enemy_y_change.append(50)   # will also move down 50px


# enemy function...
def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))


# BULLET MOCK CLASS<<<<<<<<<<<<<<<<<<<<<<<<<<<
# bullet variables...
img_bullet = pygame.image.load("bullet.png")  # 32x32px
bullet_x = 0
bullet_y = 500  # same as initial position of Rocket
bullet_x_change = 0
bullet_y_change = 1   # speed of bullet px/iteration
visible_bullet = False


# Shoot bullet function...
def shoot_bullet(x, y):
    global visible_bullet
    visible_bullet = True  # make bullet appear
    screen.blit(img_bullet, (x+16, y+10))  # bullet appears at tip of rocket


# collision detector function...
def there_is_a_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))  # pow = squared by y
    if distance < 17:
        return True
    else:
        return False


# SCOREBOARD <<<<<<<<<<<<<<<<<<<<<<<<<<
# score variables...
score = 0
my_font = pygame.font.Font('Magenta_BBT.ttf', 50)  # put source font file (not folder) in the project
text_x = 10
text_y = 10


# scoreboard function...
def show_score(x, y):
    text = my_font.render(f'score: {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


# END GAME FUNCTIONS <<<<<<<<<<<<<<<<<<<<<<
end_font = pygame.font.Font('Magenta_BBT.ttf', 80)


def final_text():
    my_final_font = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(my_final_font, (250, 200))


# GAME LOOP (live actions & presentation)<<<<<<<<<<<<<<<<<<<<<
# - watches for events in the game (such as pressing the default x button to quit)
is_running = True  # Bool switch to keep the screen open

while is_running:  # make a watcher  to put events to watched for in it.
    # Background <<<<
    # screen.fill((20, 50, 50))  # change screen background color to RGB color
    # background image...
    screen.blit(background, (0, 0))

    # demo control the players movement...
    # player_y -= 0.1  # hard-code rocket moves up each iteration

    # event handler...
    for event in pygame.event.get():  # make pygame look for a certain event
        # closing event
        if event.type == pygame.QUIT:  # when press screen X button
            is_running = False  # screen closes

        # press key events...
        if event.type == pygame.KEYDOWN:  # watch if keyboard key was pressed
            if event.key == pygame.K_LEFT:
                player_x_change = -0.2  # set movement speed to left
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.2   # set movement speed to right
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('shot.mp3')
                bullet_sound.play()
                if not visible_bullet:  # only do while a bullet is not travelling
                    bullet_x = player_x   # so the bullet has its own initial x value
                    shoot_bullet(bullet_x, bullet_y)

        # release arrow key event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0  # Stop movement

    # set player movement...
    player_x += player_x_change  # cause the rocket to move laterally via iterations

    # Set player movement constraints_7...
    # - note: upper left corner of rocket = (0,0) same for the game screen
    if player_x <= 0:  #
        player_x = 0   # 0 point of rocket width won't go pass 0 point of screen
    elif player_x >= 736:  # screen width(800) - rocket width(64) = 736
        player_x = 736

    # set enemy movement...
    for enem in range(number_of_enemies):
        # END GAME <<<<<<<<<<<<<<<<<<<
        if enemy_y[enem] > 500:  # if any of the enemy moves down 500px then do below
            for k in range(number_of_enemies):  # make all the enemies do the below
                enemy_y[k] = 1000  # move all the enemy off the screen(terrible code but works)
            final_text()  # alert the game is over
            break  # end the game loop

        # PLAY GAME <<<<<<<<<<<<<<<<<<
        enemy_x[enem] += enemy_x_change[enem]  # cause each enemy to move laterally via iterations

        #  enemy movement constraints_9...
        if enemy_x[enem] <= 0:  # when the enemy gets to the left edge:
            enemy_x_change[enem] = 0.2  # it will go right at speed of 0.3px/iteration
            enemy_y[enem] += enemy_y_change[enem]  # and will go down 50px
        elif enemy_x[enem] >= 736:  # when the enemy gets to the right edge:
            enemy_x_change[enem] = -0.2  # it will go left at speed of 0.2px/iteration
            enemy_y[enem] += enemy_y_change[enem]  # and will go down 50px
        # Collisions...
        collision = there_is_a_collision(enemy_x[enem], enemy_y[enem], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('Explosion.wav')
            collision_sound.set_volume(0.15)
            collision_sound.play()

            bullet_y = 500  # reload the player's missiles
            visible_bullet = False
            score += 1

            # reposition enemy...
            enemy_x[enem] = random.randint(0, 736)  # random position x
            enemy_y[enem] = random.randint(50, 200)  # random position y

        enemy(enemy_x[enem], enemy_y[enem], enem)  # install the enemy saucer

    # bullet reload...
    if bullet_y <= -64:  # bullet H adjustment
        bullet_y = 500   # put back in the player rocket
        visible_bullet = False  # now we can shoot another bullet
    if visible_bullet:
        shoot_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # initiate gaming objects...
    player(player_x, player_y)  # install the player rocket

    show_score(text_x, text_y)

    # update game...
    pygame.display.update()  # update the screen




