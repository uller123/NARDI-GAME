import pygame

def draw_game(screen, board, dice, turn):
    draw_board(screen, board)
    draw_dice(screen, dice)
    draw_turn(screen, turn)


def draw_board(screen, board):
    for i, stack in enumerate(board.points):
        for j, chk in enumerate(stack):
            x = i * 30
            y = 500 - j * 25 if chk.color == "black" else 50 + j * 25
            color = (0, 0, 0) if chk.color == "black" else (220, 220, 220)
            pygame.draw.circle(screen, color, (x + 15, y), 12)


def draw_dice(screen, dice):
    font = pygame.font.SysFont(None, 36)
    for i, d in enumerate(dice):
        t = font.render(str(d), True, (255, 255, 255))
        screen.blit(t, (350 + i * 40, 280))


def draw_turn(screen, turn):
    font = pygame.font.SysFont(None, 32)
    t = font.render(f"Ход: {turn}", True, (255, 255, 0))
    screen.blit(t, (10, 10))
