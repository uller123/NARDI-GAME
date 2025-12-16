from core.board import Board
from core.dice import Dice
from core.rules import collect_moves, apply_move
from core.ai import ai_random_move
from ui.render import draw_game
import pygame

def run_game(screen, clock, mode="hotseat"):
    board = Board(size=24)
    dice = Dice()

    turn = "black"
    selected = None
    dice_values = []

    running = True
    while running:
        screen.fill((80, 60, 40))
        draw_game(screen, board, dice_values, turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_SPACE and not dice_values:
                    dice_values = dice.roll()

        # AI ход
        if mode == "ai" and turn == "white" and dice_values:
            move = ai_random_move(board, "white", dice_values)
            if move:
                apply_move(board, move)
                dice_values.pop(0)
            else:
                dice_values = []
                turn = other(turn)

        # Игрок
        if mode == "hotseat" or turn == "black":
            if dice_values:
                handle_mouse(board, turn, dice_values)
                if not dice_values:
                    turn = other(turn)

        pygame.display.flip()
        clock.tick(60)


def handle_mouse(board, color, dice_values):
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        move = board.pick_move(mx, my, color, dice_values[0])
        if move:
            apply_move(board, move)
            dice_values.pop(0)


def other(c):
    return "white" if c == "black" else "black"
