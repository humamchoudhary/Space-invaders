import Singleplayer
import menu
from Buttons import Button
import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

# CONSTANTS
WIDTH, HEIGHT = 600, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
TEXT_COLOR = (255, 255, 255)

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 40)

FPS = 60
SHIP_WIDTH, SHIP_HEIGHT = 150, 150


PLAYER_ONE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets\Ships', 'InfraredFurtive.png'))

PLAYER_ONE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    PLAYER_ONE_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 0)


PLAYER_TWO_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets\Ships', 'InterstellarRunner.png'))

PLAYER_TWO_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    PLAYER_TWO_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 180)

MOVEMENT_SPEED = 10
BULLET_SPEED = 15
ROCKET_SPEED = 10
MAX_BULLETS = 2
MAX_ROCKETS = 1
PLAYER_TWO_BULLET_COLOR = (255, 0, 0)
PLAYER_ONE_BULLET_COLOR = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2, WIDTH, 5)
BORDER_COLOR = (255, 255, 255)


SPACE_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'stars_texture.png')), (WIDTH, HEIGHT))


# USER EVENTS


PLAYER_ONE_HIT_BULLET = pygame.USEREVENT + 1
PLAYER_TWO_HIT_BULLET = pygame.USEREVENT + 2
PLAYER_ONE_HIT_ROCKET = pygame.USEREVENT + 3
PLAYER_TWO_HIT_ROCKET = pygame.USEREVENT + 4

# Sounds
BULLET_SHOOT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets\Music', 'bullet.wav'))
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets\Music', 'bullet_hit.mp3'))
ROCKET_SHOOT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets\Music', 'rocket.wav'))
ROCKET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets\Music', 'bullet_hit.mp3'))
BG_MUSIC = pygame.mixer.music.load(
    os.path.join('Assets\Music', 'spaceinvaders2.wav'))

# Pause Menu Buttons
HOME_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Buttons', 'Home.png')), (90, 90))

QUIT_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Buttons', 'QuitSq.png')), (90, 90))

RESTART_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Buttons', 'Restart.png')), (90, 90))

PAUSE_MENU = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Buttons', 'PauseBg.png')), (WIDTH-200, 300))

home_btn = Button(WIDTH//2-HOME_BTN.get_width()-50,
                  HEIGHT//2-HOME_BTN.get_height()//2, HOME_BTN, HOME_BTN, WIN)

restart_btn = Button(WIDTH//2-RESTART_BTN.get_width()//2,
                     HEIGHT//2-RESTART_BTN.get_height()//2, RESTART_BTN, RESTART_BTN, WIN)

quit_btn = Button(WIDTH//2+QUIT_BTN.get_width()//2,
                  HEIGHT//2-QUIT_BTN.get_height()//2, QUIT_BTN, QUIT_BTN, WIN)
# FUNCTIONS


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullet = []
        self.cool_down_counter = 0


def Player_one_movement(keys_pressed, player_one):

    if keys_pressed[pygame.K_a] and player_one.x + MOVEMENT_SPEED > 5:  # Backwards Key
        player_one.x -= MOVEMENT_SPEED

    if keys_pressed[pygame.K_d] and player_one.x - MOVEMENT_SPEED + player_one.width + 3 < WIDTH:  # Forwards Key
        player_one.x += MOVEMENT_SPEED

    if keys_pressed[pygame.K_s] and player_one.y - MOVEMENT_SPEED > 0:  # Up Key
        player_one.y -= MOVEMENT_SPEED

    if keys_pressed[pygame.K_w] and player_one.y + MOVEMENT_SPEED + player_one.height//2+20 < BORDER.y:  # Down Key
        player_one.y += MOVEMENT_SPEED


def Player_two_movement(keys_pressed, player_one):
    if keys_pressed[pygame.K_LEFT] and player_one.x + MOVEMENT_SPEED > 0:  # BackWards Key
        player_one.x -= MOVEMENT_SPEED

    if keys_pressed[pygame.K_RIGHT] and player_one.x - MOVEMENT_SPEED + player_one.width < WIDTH - 5:  # Forwards Key
        player_one.x += MOVEMENT_SPEED

    if keys_pressed[pygame.K_UP] and player_one.y - MOVEMENT_SPEED > BORDER.y:  # Up Key
        player_one.y -= MOVEMENT_SPEED

    if keys_pressed[pygame.K_DOWN] and player_one.y + MOVEMENT_SPEED + player_one.height < HEIGHT:  # Down Key
        player_one.y += MOVEMENT_SPEED


def Move_bullets(player_one_bullets, player_two_bullets, player_one, player_two):
    for bullet in player_one_bullets:
        bullet.y += BULLET_SPEED
        if player_two.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_TWO_HIT_BULLET))
            player_one_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            player_one_bullets.remove(bullet)

    for bullet in player_two_bullets:
        bullet.y -= BULLET_SPEED
        if player_one.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_ONE_HIT_BULLET))
            player_two_bullets.remove(bullet)
        elif bullet.y < 0:
            player_two_bullets.remove(bullet)


def Move_rockets(player_one_rockets, player_two_rockets, player_one, player_two):
    for rockets in player_one_rockets:
        rockets.y += ROCKET_SPEED
        if player_two.colliderect(rockets):
            pygame.event.post(pygame.event.Event(PLAYER_TWO_HIT_ROCKET))
            player_one_rockets.remove(rockets)
        elif rockets.y > HEIGHT:
            player_one_rockets.remove(rockets)

    for rockets in player_two_rockets:
        rockets.y -= ROCKET_SPEED
        if player_one.colliderect(rockets):
            pygame.event.post(pygame.event.Event(PLAYER_ONE_HIT_ROCKET))
            player_two_rockets.remove(rockets)
        elif rockets.y < 0:
            player_two_rockets.remove(rockets)


def Winner(text):
    winner_text = WINNER_FONT.render(text, 1, TEXT_COLOR)
    dim_screen = pygame.Surface(WIN.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 180))
    WIN.blit(dim_screen, (0, 0))
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width() //
                           2, HEIGHT//2 - winner_text.get_height()//2))

    pygame.display.update()

    pygame.time.delay(2000)


def Pause():
    dim_screen = pygame.Surface(WIN.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 100))
    WIN.blit(dim_screen, (0, 0))
    WIN.blit(PAUSE_MENU, (WIDTH//2-PAUSE_MENU.get_width() //
                          2, HEIGHT//2-PAUSE_MENU.get_height()//2))
    pause_label = WINNER_FONT.render("Paused", 1, TEXT_COLOR)
    WIN.blit(pause_label, (WIDTH//2-pause_label.get_width() //
                           2, HEIGHT//2-PAUSE_MENU.get_height()//2+pause_label.get_height()//2))
    home_btn.Draw_btn()
    restart_btn.Draw_btn()
    quit_btn.Draw_btn()


def main():  # Main Function

    pygame.mixer.music.play()
    win = False
    player_two = pygame.Rect(
        WIDTH//2-PLAYER_ONE_SPACESHIP.get_width()//2, HEIGHT-200, SHIP_WIDTH, SHIP_HEIGHT)
    player_one = pygame.Rect(
        WIDTH//2-PLAYER_TWO_SPACESHIP.get_width()//2, 100, SHIP_WIDTH, SHIP_HEIGHT)

    player_one_rockets = []
    player_two_rockets = []

    player_one_bullets = []
    player_two_bullets = []

    player_two_health = 50
    player_one_health = 50
    PAUSE = False

    def draw_window(player_two, player_one, player_two_bullets, player_one_bullets, player_two_health, player_one_health, player_two_rocket, player_one_rocket):  # Drawing on screen
        WIN.blit(SPACE_BG, (0, 0))
        pygame.draw.rect(WIN, BORDER_COLOR, BORDER)
        WIN.blit(PLAYER_ONE_SPACESHIP, (player_one.x, player_one.y))
        WIN.blit(PLAYER_TWO_SPACESHIP, (player_two.x, player_two.y))
        player_two_health_text = HEALTH_FONT.render(
            "Health: " + str(player_two_health), 1, TEXT_COLOR)
        player_one_health_text = HEALTH_FONT.render(
            "Health: " + str(player_one_health), 1, TEXT_COLOR)
        WIN.blit(player_two_health_text,
                 (WIDTH - player_two_health_text.get_width() - 10, 10))
        WIN.blit(player_one_health_text, (10, 10))

        for bullet in player_two_bullets:
            pygame.draw.rect(WIN, PLAYER_TWO_BULLET_COLOR, bullet)

        for bullet in player_one_bullets:
            pygame.draw.rect(WIN, PLAYER_ONE_BULLET_COLOR, bullet)

        for rocket in player_two_rocket:
            pygame.draw.rect(WIN, PLAYER_TWO_BULLET_COLOR, rocket)

        for rocket in player_one_rocket:
            pygame.draw.rect(WIN, PLAYER_ONE_BULLET_COLOR, rocket)

        if PAUSE:
            Pause()
        pygame.display.update()

    clock = pygame.time.Clock()
    Mp_Run = True
    while Mp_Run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()
            if PAUSE:
                if home_btn.Draw_btn() and PAUSE:
                    menu.Main()
                if restart_btn.Draw_btn() and PAUSE:
                    main()
                if quit_btn.Draw_btn():
                    quit()

            # Shoot bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(player_one_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        player_one.x + player_one.width//2, player_one.y + player_one.height - 2, 5, 10)
                    player_one_bullets.append(bullet)

                    BULLET_SHOOT_SOUND.play()

                if event.key == pygame.K_RCTRL and len(player_two_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        player_two.x + player_two.width//2, player_two.y + 2, 5, 10)
                    player_two_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()

            # Shoot Rockets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    PAUSE = not PAUSE

                if event.key == pygame.K_r and len(player_one_rockets) < MAX_ROCKETS:
                    rockets = pygame.Rect(
                        player_one.x + player_one.width//2, player_one.y + player_one.height - 2, 15, 20)
                    player_one_rockets.append(rockets)
                    ROCKET_SHOOT_SOUND.play()

                if event.key == pygame.K_RALT and len(player_two_rockets) < MAX_ROCKETS:
                    rockets = pygame.Rect(
                        player_two.x + player_two.width//2, player_two.y + 2, 15, 20)
                    player_two_rockets.append(rockets)
                    ROCKET_SHOOT_SOUND.play()

            if event.type == PLAYER_ONE_HIT_BULLET:
                player_one_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == PLAYER_TWO_HIT_BULLET:
                player_two_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == PLAYER_ONE_HIT_ROCKET:
                player_one_health -= 4
                ROCKET_HIT_SOUND.play()

            if event.type == PLAYER_TWO_HIT_ROCKET:
                player_two_health -= 4
                ROCKET_HIT_SOUND.play()

        winner_text = ""

        if player_two_health <= 0:
            win = True
            winner_text = "Player One Wins!"
            PAUSE = False
            # pygame.time.delay(1000)
            # menu.Main()
        if player_one_health <= 0:
            win = True
            winner_text = "Player Two  Wins!"
            PAUSE = False
            # pygame.time.delay(1000)
            # menu.Main()
        if winner_text != "":
            Winner(winner_text)
            pygame.time.delay(1000)
            menu.Main()

        Move_bullets(player_one_bullets, player_two_bullets,
                     player_one, player_two)
        Move_rockets(player_one_rockets, player_two_rockets,
                     player_one, player_two)

        keys_pressed = pygame.key.get_pressed()
        # Movements for Player_one_Ship
        Player_one_movement(keys_pressed, player_one)
        Player_two_movement(keys_pressed, player_two)

        # Drawing n screen
        draw_window(player_two, player_one, player_two_bullets, player_one_bullets,
                    player_two_health, player_one_health, player_two_rockets, player_one_rockets)

    main()


if __name__ == "__main__":
    main()
