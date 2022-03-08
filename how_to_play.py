
import pygame
from Buttons import Button
import os
import menu

pygame.font.init()
pygame.mixer.init()
pygame.init()


# constants
FONT = pygame.font.SysFont('comicsans', 30)
SEC_FONT = pygame.font.SysFont('comicsans', 22)
TEXT_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 600, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

HEAD_IMG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'head.png')), (WIDTH, HEIGHT)).convert_alpha()

BACK_BTN = pygame.transform.scale(pygame.image.load(
    'Assets\Buttons\Back.png').convert_alpha(), (60, 60))

SPACE_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'stars_texture.png')), (WIDTH, HEIGHT))

MENU_BG = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets\Buttons', 'Menu-bg.png')), (WIDTH-80, HEIGHT-140))

back_btn = Button(10, 10, BACK_BTN, BACK_BTN, WIN)


def Set_Draw(y, Text_list):
    WIN.blit(SPACE_BG, (0, 0))
    WIN.blit(MENU_BG, (40, 100))
    Text_Draw.Draw(Text_Draw(Text_list, y), WIN)
    WIN.blit(HEAD_IMG, (0, 0))
    back_btn.Draw_btn()
    screen_label = FONT.render("How To Play", 1, TEXT_COLOR)
    WIN.blit(screen_label, (WIDTH//2 - screen_label.get_width()//2, 10))
    WIN.blit(HEAD_IMG, (0, 705))


class Text_Draw:
    Text_Map = {
        1: "Dont let the eneimes hit the lower part of the screen",
        2: "If an enemy hits the bottom of the screen you will lose 1 live",
        3: "Get as much highscore as possible"
    }

    def __init__(self, text, y, color=TEXT_COLOR):
        self.text = text
        self.y = y
        self.color = color

    def Draw(self, window):
        for text in self.text:
            label = SEC_FONT.render(text, 1, TEXT_COLOR)
            window.blit(
                label, (WIDTH//2-label.get_width() // 2, self.y+30*self.text.index(text)))


def Main():
    y = 120
    clock = pygame.time.Clock()
    Text_list = ["Controls for single player:", "A and D to move the player ship", "SPACE to shoot bullets", "P to pause the game", "Q to exit out of the game",
                 "Rules for single player:", "Dont let the enemy ships hit ", "the bottom of the screen", "If an enemy hits the bottom of the screen ", "you will lose 1 live", "enemies get faster with time",
                 "If you lose all the live or", "lose all the health you lose", "try to beat the high score", "watch out how you use our bullets as ", "they are limited.",
                 "WASD to move the ship", "RIGHT CTRL shoot bullets and ", "RIGHT ALT to shoot rockets",
                 "Kill the opposing player before getting eliminated.", "You have unlimited ammo but it has a cool down"]
    crun = True
    while crun:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if back_btn.Draw_btn():
                menu.Main()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and y > 60:
            y -= 2
        if keys[pygame.K_s]:
            if y < 120:
                y += 2

        Set_Draw(y, Text_list)
        pygame.display.update()


if __name__ == "__main__":
    Main()
