import pygame
import random


class Cube:
    def __init__(self):
        self.imageE = pygame.transform.scale(pygame.image.load("Images/f.png"), (100, 100))

    cube_list = [pygame.transform.scale(pygame.image.load("Images/куб1.png"), (30, 30)),
                 pygame.transform.scale(pygame.image.load("Images/куб2.png"), (30, 30)),
                 pygame.transform.scale(pygame.image.load("Images/куб3.png"), (30, 30)),
                 pygame.transform.scale(pygame.image.load("Images/куб4.png"), (30, 30)),
                 pygame.transform.scale(pygame.image.load("Images/куб5.png"), (30, 30)),
                 pygame.transform.scale(pygame.image.load("Images/куб6.png"), (30, 30))]

    def throw_cubs(self, screen, clock):
        stac = pygame.transform.scale(
            pygame.image.load("Images/ведро.png"),
            (832 * 0.1, 1216 * 0.1))
        dec = pygame.transform.scale(
            pygame.image.load("Images/доска.png"),
            (600, 600))
        for i in range(20):
            screen.blit(dec, (0, 0))
            screen.blit(stac, (520, 380 + (-1) ** i * 10))
            pygame.display.update()
            clock.tick(15)
        first, second = random.randint(1, 6), random.randint(1, 6)
        self.first_сube = first - 1
        self.second_сube = second - 1
        return [first, second]

    first_сube = 0
    second_сube = 0

    def prin_cube(self, screen, was_thrown):
        screen.blit(self.cube_list[self.first_сube], (550, 400))
        screen.blit(self.cube_list[self.second_сube], (550, 450))
        if not was_thrown:
            screen.blit(self.imageE, (250, 250))