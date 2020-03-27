from __future__ import division
import random
import pygame
from os import path


# record the path of folders pics&sounds




# define menu
def menu():
    global screen 
    
    # load and play the music for the menu
    pygame.mixer.music.load(path.join(sound_folder, "menu.ogg")) #############
    pygame.mixer.music.play(-1)
    
    # load the menu pic and 
    title = pygame.image.load(path.join(img_folder, "menu.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
    
    # 实现动画效果
    screen.blit(title, (0, 0))
    pygame.display.update()
    
    while True:
        # it is like a get()
        move = pygame.event.poll() 
        
        if move.type == pygame.KEYDOWN:
            if move.key == pygame.K_q:
                pygame.quit()
                quit()
            elif move.key == pygame.K_RETURN:
                break
            else:
                continue
        elif move.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            # "+" moves words down not up!
            show_words(screen, "Welcome to Bug Shooter!", 40, WIDTH/2, (HEIGHT/2)-275)
            show_words(screen, "Press [return] to start", 40, WIDTH/2, (HEIGHT/2)+150)
            show_words(screen, "or [q] to quit.", 40, WIDTH/2, (HEIGHT/2)+200)
            pygame.display.update()
        
        
    # stop the music
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    screen.fill(BLUE)
    show_words(screen, "GET READY!", 50, WIDTH/2, HEIGHT/2)
    pygame.display.update()




# make the words show on the menu
def show_words(surf, text, size, x, y):
    ## we need a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    # rect is a rectangle
    text_rect = text_surface.get_rect()  
    text_rect.midtop = (x, y)  
    surf.blit(text_surface, text_rect) 
    
    
    
    
# show how many lives are left
def lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)





# show how much blood one life has
def blood(surf, x, y, percentage):
    percentage = max(percentage, 0) 
    fill = (percentage / 100) * BLOOD_LENGTH
    outline_rect = pygame.Rect(x, y, BLOOD_LENGTH, BLOOD_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BLOOD_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)







# bug is the ones that you need to shoot
def newbug():
    bug_element = Bug()
    all_sprites.add(bug_element)
    bugs.add(bug_element)



# make the special effect of explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# class the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # make the player pic slower
        self.image = pygame.transform.scale(player_img, (50*3, 37*3))
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.speedx = 0 
        self.shield = 100
        # set the shoot_delay to make the game harder
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()



    def update(self):
        # time out for powerups ???????????????????????????????
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide ???????????????????????????????????????????????
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 5

        # position
        self.speedx = 0
        # move the shooter left or right
        # return a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()
            
        # the shooter cannot go out of the screen
        # check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx





    def shoot(self):
        # to tell the bullet where to shoot
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # we can have one or two or three bullets
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # Missile shoots from center of ship
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def more_bullets(self):
        # add more bullets if get bubbletea
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# class the bugs
class Bug(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images) 
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        # randomize the speed of the bug
        # change the speed to make the game more difficult
        self.speedy = random.randrange(5, 15)        

        # randomize the movements
        self.speedx = random.randrange(-3, 3)

        # adding rotation to the bug element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        # time when the rotation has to happen
        self.last_time = pygame.time.get_ticks()
        
    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time > 50:
            self.last_time = current_time
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # now what if the bug element goes out of the screen
        if (self.rect.top > HEIGHT + 10)\
             or (self.rect.left < -25)\
             or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            # randomize the speed of the bug
            self.speedy = random.randrange(1, 8)    





## class the sprite for more bullets
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'flash'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # place the bullet according to the current position of the shooter
        # bullets need to be placed right infront of the shooter
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill the sprite after it moves over the top border
        if self.rect.top > HEIGHT:
            self.kill()





# defines the sprite for bullets
# sprite is the 精灵模块 it makes animation
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()




# set the missile
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()




#------------------------------- load pics ------------------------------------

img_folder = path.join(path.dirname(__file__), "pics")
sound_folder = path.join(path.dirname(__file__), "sounds")

# set the basic variables
WIDTH = 480
HEIGHT = 600
# it is the spped of the shooter
FPS = 60 
# the time that a flash works
POWERUP_TIME = 5000 
BLOOD_LENGTH = 100 
BLOOD_HEIGHT = 10 

# set the frequently used colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# initialize pygame and open a window
pygame.init()
# put in the music
pygame.mixer.init()
#display the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# set the game name
pygame.display.set_caption("Bug Shooter")
# sync the FPS
clock = pygame.time.Clock()
# set the font 
font_name = pygame.font.match_font("arial")
##------
background = pygame.image.load(path.join(img_folder, 'background.png')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_folder, 'shooter.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_folder, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_folder, 'missile.png')).convert_alpha()
# meteor_img = pygame.image.load(path.join(img_folder, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    'bugbug1.png',
    'bugbug2.png', 
    'bugbug3.png', 
    'bugbug4.png',
    'bugbug5.png',
    'bugbug6.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_folder, image)).convert())

# meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    # resize the explosion
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    # player explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)



# load power ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['flash'] = pygame.image.load(path.join(img_folder, 'bolt_gold.png')).convert()




#------------------------------ load sounds -----------------------------------
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
# main background music
# simmered the sound down a little
pygame.mixer.music.set_volume(0.2)

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))











#--------------------------------- Game loop ----------------------------------
running = True
menu_display = True
while running:
    if menu_display:
        menu()
        pygame.time.wait(3000)

        # Stop menu music
        pygame.mixer.music.stop()
        # Play the game music
        pygame.mixer.music.load(path.join(sound_folder, 'game.ogg'))
        # makes the game music in an endless loop
        pygame.mixer.music.play(-1)   
        
        menu_display = False
        
        # group all the sprites together for ease of update
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        # spawn a group of mob
        bugs = pygame.sprite.Group()
        # this controls the frequency of the bugs\
        # or, that is, the frequency of new bugs popping up
        for i in range(8):     
            newbug()

        # group for bullets
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # Score board variable
        # i am thinking about sending the score to the server to compete?????????????????????
        score = 0
    #1 Process input/events
    # will make the loop run at the same speed all the time
    clock.tick(FPS)    
    # gets all the events which have occured till now and keeps tab of them.
    for event in pygame.event.get():       
        # press the X button at the top
        if event.type == pygame.QUIT:
            running = False

        # Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
      
    #2 Update
    all_sprites.update()

    # check if a bullet hit a bug
    # we have a group of bullets and a group of mob
    hits = pygame.sprite.groupcollide(bugs, bullets, True, True)
    ## now as we delete the mob element when we hit one with a bullet, we need to respawn them again
    ## as there will be no mob_elements left out 
    for hit in hits:
        score += 50 - hit.radius         ## give different scores for hitting big and small metoers
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            power = Power(hit.rect.center)
            all_sprites.add(power)
            powerups.add(power)
        # spawn a new bug
        newbug()        
    # ^^ the above loop will create the amount of mob objects which were killed spawn again

    # check if the player collides with the bug
    # gives back a list, True makes the bug element disappear
    hits = pygame.sprite.spritecollide(player, bugs, True, pygame.sprite.collide_circle)      
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newbug()
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100

    ## if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'flash':
            player.more_bullets()

    ## if player died and the explosion has finished, end game
    if player.lives == 0 and not death_explosion.alive():
        running = False

    #3 Draw/render
    screen.fill(BLACK)
    # draw the stargaze.png image
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    show_words(screen, str(score), 30, WIDTH / 2, 10)     ## 10px down from the screen
    blood(screen, 10, 5, player.shield)

    # Draw lives
    lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()


