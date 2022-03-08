from Buttons import Button
import Singleplayer
import how_to_play
import multiplayer
import settings
import pygame
import os

# Insializing pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Importing Game screens

# Button

# Constants


# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

FONT = pygame.font.SysFont('comicsans', 30)

WIDTH, HEIGHT = 600, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADERS 'RELIVING THE CHILDHOOD'")
BG_IMG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'stars_texture.png')), (WIDTH, HEIGHT))


# Buttons
BUTTON_SIZE = (261, 68)

START_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Start.png')), BUTTON_SIZE).convert_alpha()

START_HOV = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Start_hov.png')), BUTTON_SIZE).convert_alpha()

SETTING_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Settings.png')), BUTTON_SIZE).convert_alpha()

SETTING_HOV = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Setting_hov.png')), BUTTON_SIZE).convert_alpha()

CONTROL_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Controls.png')), BUTTON_SIZE).convert_alpha()

CONTROL_HOV = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Control_hov.png')), BUTTON_SIZE).convert_alpha()

QUIT_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Quit.png')), BUTTON_SIZE).convert_alpha()

QUIT_HOV = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Quit_hov.png')), BUTTON_SIZE).convert_alpha()

MENU_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Menu-bg.png')), (282, 365)).convert_alpha()

MENU_HEADING = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\Menu-Heading.png')), BUTTON_SIZE).convert_alpha()
SP_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\sp_BTN.png')), BUTTON_SIZE).convert_alpha()

SP_BTN_HOV = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\sp_BTN_hov.png')), BUTTON_SIZE).convert_alpha()

MP_BTN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\MP_btn.png')), BUTTON_SIZE).convert_alpha()

MP_BTN_HOV = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Buttons\MP_btn_hov.png')), BUTTON_SIZE).convert_alpha()

MENU_BG_LOCx, MENU_BG_LOCy = (WIDTH//2-(282//2), HEIGHT//2)  # (11,67)
LOGO_WIDTH = WIDTH-200
LOGO_HEIGTH = LOGO_WIDTH/3
LOGO = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Logo.png')), (LOGO_WIDTH, LOGO_HEIGTH)).convert_alpha()

BACKGROUND_MUSIC = pygame.mixer.music.get_volume()

PAUSE_MENU = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Buttons', 'PauseBg.png')), (WIDTH-200, 300))
# Functions


start_btn = Button(MENU_BG_LOCx+11, MENU_BG_LOCy+67, START_BTN, START_HOV, WIN)
settings_btn = Button(MENU_BG_LOCx+11, MENU_BG_LOCy +
                      (67*2), SETTING_BTN, SETTING_HOV, WIN)
control_btn = Button(MENU_BG_LOCx+11, MENU_BG_LOCy +
                     (67*3), CONTROL_BTN, CONTROL_HOV, WIN)
quit_btn = Button(MENU_BG_LOCx+11, MENU_BG_LOCy +
                  (67*4), QUIT_BTN, QUIT_HOV, WIN)
back_btn = settings.back_btn

mode_label = FONT.render("Chose a game mode", 1, WHITE)

sngplr_btn = Button(WIDTH//2-SP_BTN.get_width()//2, HEIGHT//2-PAUSE_MENU.get_width() //
                    2+mode_label.get_height()+SP_BTN.get_height(), SP_BTN, SP_BTN_HOV, WIN)

mltplr_btn = Button(WIDTH//2-MP_BTN.get_width()//2, HEIGHT//2-PAUSE_MENU.get_width() //
                    2+mode_label.get_height()+MP_BTN.get_height()*2, MP_BTN, MP_BTN_HOV, WIN)


def Main():
    Menu_run = True
    pygame.mixer.music.play()
    Game_Menu = False

    def Menu_Draw():

        WIN.blit(BG_IMG, (0, 0))
        if not Game_Menu:
            WIN.blit(MENU_BG, (MENU_BG_LOCx, MENU_BG_LOCy))
            WIN.blit(MENU_HEADING, (MENU_BG_LOCx+11, MENU_BG_LOCy+10))
            WIN.blit(LOGO, ((WIDTH//2)-(LOGO_WIDTH//2), 100))
            start_btn.Draw_btn()
            settings_btn.Draw_btn()
            control_btn.Draw_btn()
            quit_btn.Draw_btn()

        if Game_Menu:

            WIN.blit(PAUSE_MENU, (WIDTH//2-PAUSE_MENU.get_width() //
                                  2, HEIGHT//2-PAUSE_MENU.get_width()//2))
            WIN.blit(mode_label, (WIDTH//2-mode_label.get_width() // 2,
                                  HEIGHT//2-PAUSE_MENU.get_width()//2+mode_label.get_height()+20))
            back_btn.Draw_btn()
            mltplr_btn.Draw_btn()
            sngplr_btn.Draw_btn()
        pygame.display.update()

    clock = pygame.time.Clock()

    while Menu_run:
        clock.tick(60)
        Menu_Draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Menu_run = False
            if start_btn.Draw_btn():
                print("Start")
                Game_Menu = True
            if settings_btn.Draw_btn():
                settings.Main()
            if control_btn.Draw_btn():
                print("Controls")
                how_to_play.Main()
            if quit_btn.Draw_btn():
                print("Quit")
                Menu_run = False
                quit()
            if back_btn.Draw_btn():
                Game_Menu = False
            if sngplr_btn.Draw_btn() and Game_Menu:
                print("Going to Single Player")
                Singleplayer.Main_SP()
            if mltplr_btn.Draw_btn() and Game_Menu:
                print("Going to Multiplayer")
                multiplayer.main()


if __name__ == '__main__':
    Main()
