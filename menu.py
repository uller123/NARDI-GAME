from Game import *
from GameControl import *


def start_menu():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 600))
    back_ground = pygame.transform.scale(pygame.image.load("Images/сизо.png"), (1280 // 2, 720))
    star_game_button = pygame.transform.scale(pygame.image.load("Images/кнопкаНачатьИгру.png"), (448 * 0.6, 99 * 0.6))
    star_game_button_rect = star_game_button.get_rect(topleft=(180, 300))
    win_black_image = pygame.transform.scale(pygame.image.load("Images/черныйИгрок.png"), (720, 720))
    win_white_image = pygame.transform.scale(pygame.image.load("Images/белыйИгрок.png"), (720, 720))
    running = True
    while running:
        pygame.display.update()
        screen.blit(back_ground, (-20, -100))
        screen.blit(star_game_button, (180, 300))

        mouse = pygame.mouse.get_pos()
        if star_game_button_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            win_color = start_game(screen, clock)
            if win_color == "Black":
                back_ground = win_black_image
            if win_color == "White":
                back_ground = win_white_image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        clock.tick(60)


if __name__ == "__main__":
    start_menu()