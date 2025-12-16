import pygame
from core.game import run_game

WIDTH, HEIGHT = 800, 600

def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 48)

    running = True
    while running:
        screen.fill((30, 30, 30))

        text = font.render("НАРДЫ — НАЖМИ ENTER", True, (200, 200, 200))
        screen.blit(text, (200, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run_game(screen, clock, mode="hotseat")
                if event.key == pygame.K_a:
                    run_game(screen, clock, mode="ai")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
