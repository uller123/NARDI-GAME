import pygame
from game import run_game

WIDTH, HEIGHT = 900, 600

def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nardi")

    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))
        text = font.render("Press ENTER to Start", True, (240, 240, 240))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                run_game(screen)

        pygame.display.flip()
        clock.tick(60)
