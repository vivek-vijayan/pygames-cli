# %% Importing all necessary libraries
import os
import pygame as pg
import sys
import typing
import random


# %% Initialising the fonts and mixer
pg.font.init()
# pg.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pg.init()

# %% pre-defining the window properties
WIDTH, HEIGHT = 700, 700
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Aero Shooter Game")


# %% Defining the colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


# %% Game properties
FPS = 60
VELOCITY = 10
BULLET_VELOCITY = 10
MAX_BULLET = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 70
clock = pg.time.Clock()

# %% Score
score_gained = 0

# %% Fire hit
ENEMY_HIT = pg.USEREVENT + 1

# %% Fonts register
SCORE = pg.font.SysFont('comicsans', 20)
LIVES = pg.font.SysFont('comicsans',18)

# %% Fire sound MP3 loader
FIRESOUND = pg.mixer.Sound("aero-shoot-supports/fire-sound.wav")
BGM = pg.mixer.Sound("aero-shoot-supports/bgm.wav")
BGM.play()  # Playing the BGM once loaded

# %% Blast sound
BLAST_SOUND = pg.mixer.Sound("aero-shoot-supports/blast.wav")

# %% Spaceship image
SPACESHIP_IMAGE_LOAD = pg.image.load("aero-shoot-supports/spaceship.png")
A_SPACESHIP = pg.transform.scale(
    SPACESHIP_IMAGE_LOAD, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)



# %% Aliens
ALIENS_IMAGE_LOAD = pg.image.load("aero-shoot-supports/aliens.png")
ALIEN_SPACESHIP = pg.transform.scale(
    ALIENS_IMAGE_LOAD, ((SPACESHIP_WIDTH - 20), (SPACESHIP_HEIGHT - 20))
)

# %% Spaceship bullet fire
A_FIRE = pg.image.load("aero-shoot-supports/ship-model-1-fire.png")
FIRE = pg.transform.scale(A_FIRE, (70, 70))

# %% Space background
SPACE_BACKGROUND_LOAD = pg.image.load("aero-shoot-supports/background.jpeg")
SPACE_BG = pg.transform.scale(SPACE_BACKGROUND_LOAD, (WIDTH, HEIGHT))

# %% Heart Image load
HEART_IMAGE_LOAD = pg.image.load("aero-shoot-supports/heart.png")
HEART = pg.transform.scale(HEART_IMAGE_LOAD, (30,30))

# %% Handle bullets
def shootBullet(bulletsList: typing.List, active_aliens, score) -> int:
    for eachBullet in bulletsList:
        eachBullet["y-param"] -= 5

        if eachBullet["y-param"] < 0:
            bulletsList.remove(eachBullet)

        for eachAlien in active_aliens: 
            if (eachBullet["y-param"] <= eachAlien['y-param'] and (eachBullet['x-param'] < (eachAlien['x-param'] + 20) and eachBullet['x-param'] > (eachAlien['x-param'] -20 ))): 
                bulletsList.remove(eachBullet)
                active_aliens.remove(eachAlien)
                BLAST_SOUND.play()
                score +=10
    return score

# %% Arrival of the alien spaceship
def alien_arrival(alien_count) -> int:
    for eachAlien in alien_count:
        eachAlien["y-param"] += 2

        if eachAlien["y-param"] > HEIGHT:
            alien_count.remove(eachAlien)
            return 1
    return 0



# %% Game functions
def draw_game_window(Bullet, spaceship_parameter, bulletList,alienList, score, lives):
    WIN.blit(SPACE_BG, (0, 0))
    WIN.blit(A_SPACESHIP, (spaceship_parameter.x, spaceship_parameter.y))  # spaceship
    score_text = SCORE.render("Score : " + str(score),1,YELLOW) 
    WIN.blit(score_text, (WIDTH- score_text.get_width() - 30, 20))   # score screen
    WIN.blit(HEART, (30,20))
    lives_pending = LIVES.render(" " + str(lives), 1, WHITE)
    WIN.blit(lives_pending, (60,20))

    for bullet in bulletList:
        WIN.blit(bullet["bullet"], (bullet["x-param"], bullet["y-param"]))

    for alien in alienList:
        WIN.blit(alien["alien"], (alien["x-param"], alien["y-param"]))
    # last statement
    pg.display.update()


# %% Main function
def main():
    gamerun = True
    gameplay = False
    bullets = []
    aliens_count = 10
    score_gained = 0
    lives_pending = 5
    aliens = []
    spaceship_parameter = pg.Rect(
        (WIDTH // 2) - 70, HEIGHT - 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
    )
    while gamerun:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gamerun = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ENTER:
                    gameplay = True

                if event.key == pg.K_SPACE and len(bullets) < 3:
                    # Adding bullets to shooting gun
                    each_bullet = {
                        "bullet": FIRE,
                        "x-param": spaceship_parameter.x,
                        "y-param": spaceship_parameter.y,
                    }
                    bullets.append(each_bullet)
                    FIRESOUND.play()

                    each_alien = {
                        "alien": ALIEN_SPACESHIP,
                        "x-param": int(random.randint(10, WIDTH - 10)),
                        "y-param": 0,
                    }
                    aliens.append(each_alien)

        # Spaceship movement
        keypressed = pg.key.get_pressed()
        if keypressed[pg.K_LEFT]:
            spaceship_parameter.x -= 5
        if keypressed[pg.K_RIGHT]:
            spaceship_parameter.x += 5

        
        # end line refresher with updates
        score_gained = shootBullet(bullets, aliens, score_gained)
        lives_pending -= alien_arrival(aliens)
        draw_game_window(1, spaceship_parameter, bullets, aliens, score_gained, lives_pending)




# %% Main execution

if __name__ == "__main__":
    main()
