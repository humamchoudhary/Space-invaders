import menu
import highscore
import time
import pygame
import os
from random import *
from Buttons import Button
import sys

pygame.init()
pygame.mixer.init()
pygame.font.init()

# Inisializing the constants
WIDTH, HEIGHT = 600, 750
SHIP_WIDTH = 200
SHIP_HEIGHT = 200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders 'Reliving the childhood'")
BG_IMG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'stars_texture.png')), (WIDTH, HEIGHT))

PLAYER_SHIP_1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets\Ships', 'InfraredFurtive.png')),  180), (SHIP_WIDTH, SHIP_HEIGHT)).convert_alpha()

Player_Bullet = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets\Ships', 'player_bullet.png')), 180).convert_alpha()

ENEMY_BULLET = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets\Ships', 'enemy_bullet.png')), 180).convert_alpha()

ENEMY_SHIP_1 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Ships', 'Warship.png')),  (SHIP_WIDTH, SHIP_HEIGHT)).convert_alpha()

ENEMY_SHIP_2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Ships', 'InterstellarRunner.png')), (SHIP_WIDTH, SHIP_HEIGHT)).convert_alpha()

ENEMY_SHIP_3 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Ships', 'Transtellar.png')), (SHIP_WIDTH, SHIP_HEIGHT)).convert_alpha()

ENEMY_SHIP_4 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Ships', 'GalactixRacer.png')), (SHIP_WIDTH, SHIP_HEIGHT)).convert_alpha()

BULLET_SHOOT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets\Music', 'bullet_hit.mp3'))

BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets\Music', 'bullet.wav'))

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
BULLET_VEL = 5
MAX_BULLETS = 3
TEXT_COLOR = (255, 255, 255)
END_FONT = pygame.font.SysFont('comicsans', 50)


class Bullet:

    def __init__(self, x, y, img, axis=0):
        self.x = x+choice([30, 70])
        self.y = y+(SHIP_HEIGHT/2*axis)
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)

    def Draw_bullet(self, window, axis=0):
        # mask_surf = self.mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))         #Pixel Perfect Hitbox
        # window.blit(mask_surf, (self.x, self.y))

        window.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(window, TEXT_COLOR, pygame.Rect(
        # self.x+47, self.y+30, self.img.get_width()-90, self.img.get_height()-60))  # Bullet Hitbox

    def Bullet_Move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y + 50 >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def Get_rect(self):
        return pygame.Rect(
            self.x+47, self.y+30, self.img.get_width()-90, self.img.get_height()-60)


class Ship:
    COOLDOWN = 25

    def __init__(self, x, y, width, height, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.bullet = None
        self.bullets = []
        self.bullet_img = None
        self.cool_down = 0
        self.width = width
        self.height = height

    def Draw(self, window, axis=0):
        # mask_surf = self.mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))         #Pixel Perfect Hitbox

        # pygame.draw.rect(window, TEXT_COLOR,
        #  pygame.Rect(self.x+50, self.y+50, SHIP_WIDTH/2, SHIP_HEIGHT/2))  # Ship HitBox

        for bullet in self.bullets:
            bullet.Draw_bullet(window, axis)
        window.blit(self.img, (self.x, self.y))
        # window.blit(mask_surf, (self.x, self.y))

    def Move_bullet(self, vel, obj):
        self.Shoot_cooldown()
        for bullet in self.bullets:
            bullet.Bullet_Move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)

            elif bullet.collision(obj):
                # elif pygame.Rect.colliderect(bullet.Get_rect(), obj.Get_rect()):
                obj.health -= 10
                self.bullets.remove(bullet)

    def Shoot_cooldown(self):
        if self.cool_down >= self.COOLDOWN:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def Shoot(self, total_bullets, axis=0):
        if self.cool_down == 0 and len(self.bullets) < MAX_BULLETS and total_bullets != 0:
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            total_bullets -= 1
            self.cool_down = 1
        return total_bullets

    def Get_rect(self):
        return pygame.Rect(self.x+50, self.y+50, SHIP_WIDTH/2, SHIP_HEIGHT/2)

    def Get_width(self):
        return self.img.get_width()

    def Get_height(self):
        return self.img.get_height()


class Player(Ship):
    def __init__(self, x, y, width, height, health=100):
        super().__init__(x, y, width, height, health)
        self.img = PLAYER_SHIP_1
        self.bullet_img = Player_Bullet
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health

    def Get_rect(self):
        return pygame.Rect(self.x+50, self.y+50, SHIP_WIDTH/2, SHIP_HEIGHT/2)

    def Shoot(self, total_bullets, axis=0):
        if self.cool_down == 0 and len(self.bullets) < MAX_BULLETS and total_bullets != 0:
            BULLET_SHOOT_SOUND.play()
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            total_bullets -= 1
            self.cool_down = 1
        return total_bullets

    def Hit_Enemy(self, enemies):
        for enemy in enemies:
            if self.collision(enemy):
                self.health -= 30
                enemies.remove(enemy)

    def collision(self, obj):
        return collide(self, obj)

    def Move_bullet(self, vel, objs, enemies_killed):
        self.Shoot_cooldown()
        for bullet in self.bullets:
            bullet.Bullet_Move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    # if pygame.Rect.colliderect(bullet.Get_rect(), obj.Get_rect()):
                    if bullet.collision(obj):
                        # if pygame.sprite.collide_mask(obj, bullet) != None:
                        objs.remove(obj)
                        enemies_killed += 1
                        self.bullets.remove(bullet)
        return enemies_killed


class Enemy(Ship):
    SKIN_MAP = {
        "enemy1": ENEMY_SHIP_1,
        "enemy2": ENEMY_SHIP_2,
        "enemy3": ENEMY_SHIP_3,
        "enemy4": ENEMY_SHIP_4,
    }

    def __init__(self, x, y, width, height, skin, health=20):
        super().__init__(x, y, width, height, health)
        self.bullet_img = ENEMY_BULLET
        self.img = self.SKIN_MAP[skin]
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)

    def Movement_enemy(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def Main_SP():
    start_time = time.time()

    Sp_Run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 20)
    clock = pygame.time.Clock()
    player_veloctiy = 5
    player = Player(WIDTH//2-SHIP_WIDTH//2, HEIGHT -
                    SHIP_HEIGHT//2 - 60, SHIP_WIDTH, SHIP_HEIGHT)

    enemies = []
    total_bullets = 1
    enemy_vel = 1
    wave_length = 0
    lost_count = 0
    lost = False
    pause = False
    enemies_killed = 0
    passed_time = 0

    def Draw_Main(time, enemies_killed):
        WIN.blit(BG_IMG, (0, 0))

        for enemy in enemies:
            enemy.Draw(WIN, 1)
        player.Draw(WIN)
        # HUD

        lives_label = main_font.render(f"Lives: {lives}", 1, TEXT_COLOR)

        level_label = main_font.render(f"Level: {level}", 1, TEXT_COLOR)

        WIN.blit(lives_label, (10, 10))

        WIN.blit(level_label, (WIDTH - level_label.get_width()-10, 10))

        enemy_left_label = main_font.render(
            f"Enemies Left: {len(enemies)}", 1, TEXT_COLOR)

        WIN.blit(enemy_left_label, (10, HEIGHT -
                                    enemy_left_label.get_height()-10))
        enemy_killed_label = main_font.render(
            f"Enemies Killed: {enemies_killed}", 1, TEXT_COLOR)

        WIN.blit(enemy_killed_label, (10, HEIGHT -
                                      enemy_left_label.get_height()-40))

        bullet_left_label = main_font.render(
            f"Bullets left: {total_bullets}", 1, TEXT_COLOR)

        WIN.blit(bullet_left_label, (WIDTH - bullet_left_label.get_width() -
                                     10, HEIGHT - bullet_left_label.get_height()-10))
        player_health_label = main_font.render(
            f"Health = {player.health}", 1, TEXT_COLOR)
        WIN.blit(player_health_label, (WIDTH - player_health_label.get_width() -
                                       10, HEIGHT - (bullet_left_label.get_height()+player_health_label.get_height()+5)))
        score = time + time * enemies_killed

        time_label = main_font.render(
            f"Score: {score}", 1, TEXT_COLOR)
        WIN.blit(time_label, (WIDTH//2-time_label.get_width()//2, 10))

        if lost:
            lost_label = END_FONT.render("You Lost!!", 1, TEXT_COLOR)
            WIN.blit(lost_label, (WIDTH//2-lost_label.get_width() //
                                  2, HEIGHT//2-lost_label.get_height()//2))
            score = time + time * enemies_killed
            score_label = main_font.render(
                f"Your Score: {score}", 1, TEXT_COLOR)
            WIN.blit(score_label, (WIDTH//2-score_label.get_width() //
                                   2, HEIGHT//2+score_label.get_height()))
            high_score = highscore.Get_High(score)
            high_score_label = main_font.render(
                f"High Score: {high_score}", 1, TEXT_COLOR)
            WIN.blit(high_score_label, (WIDTH//2 -
                                        high_score_label.get_width()//2, HEIGHT//2+score_label.get_height()+high_score_label.get_height()))
            if int(score) >= int(high_score):
                high_label = main_font.render("New High Score!", 1, TEXT_COLOR)
                WIN.blit(high_label, (WIDTH//2-high_score_label.get_width()//2, HEIGHT//2 +
                                      score_label.get_height()+high_score_label.get_height()+high_label.get_height()))
            pygame.display.update()
            pygame.time.delay(2000)
            menu.Main()

        if pause:
            dim_screen = pygame.Surface(WIN.get_size()).convert_alpha()
            dim_screen.fill((0, 0, 0, 100))
            WIN.blit(dim_screen, (0, 0))
            WIN.blit(PAUSE_MENU, (WIDTH//2-PAUSE_MENU.get_width() //
                                  2, HEIGHT//2-PAUSE_MENU.get_height()//2))
            pause_label = END_FONT.render("Paused", 1, TEXT_COLOR)
            WIN.blit(pause_label, (WIDTH//2-pause_label.get_width() //
                                   2, HEIGHT//2-PAUSE_MENU.get_height()//2+pause_label.get_height()//2))
            home_btn.Draw_btn()
            restart_btn.Draw_btn()
            quit_btn.Draw_btn()

        pygame.display.update()
    while Sp_Run:
        clock.tick(FPS)
        Draw_Main(int(passed_time), enemies_killed)
        player.Hit_Enemy(enemies)
        if lives <= 0 or player.health <= 0:
            lost = True

        if lost:
            pass

        if len(enemies) == 0:
            level += 1
            enemy_vel += 0.5
            wave_length += 5
            total_bullets += wave_length + 3
            for i in range(wave_length):
                enemy = Enemy(randrange(30, WIDTH - SHIP_WIDTH), randrange(-500*wave_length//3, -100),
                              SHIP_WIDTH, SHIP_HEIGHT, choice(["enemy1", "enemy2", "enemy3", "enemy4"]))
                enemies.append(enemy)
            if player.health != 100:
                player.health += 20*level
                if player.health > 100:
                    player.health = 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if home_btn.Draw_btn():
                menu.Main()
            if restart_btn.Draw_btn():
                Main_SP()
            if quit_btn.Draw_btn():
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause

                if event.key == pygame.K_ESCAPE:
                    Sp_Run = False
                if event.key == pygame.K_l:
                    lost = True

        keys = pygame.key.get_pressed()

        # Draw Pause menu

        if not pause:
            passed_time = time.time() - start_time
            if keys[pygame.K_a] and player.x + 30 > 0:
                player.x -= player_veloctiy

            if keys[pygame.K_d] and player.x < WIDTH:
                player.x += player_veloctiy

            if keys[pygame.K_SPACE]:
                total_bullets = player.Shoot(total_bullets)

            for enemy in enemies[:]:
                enemy.Movement_enemy(enemy_vel)
                enemy.Move_bullet(BULLET_VEL, player)
                if randrange(0, 3*60) == 1:
                    enemy.Shoot(100)
                if enemy.y > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)
            enemies_killed = player.Move_bullet(-BULLET_VEL,
                                                enemies, enemies_killed)
        else:
            start_time = time.time() - passed_time


if __name__ == "__main__":
    Main_SP()
