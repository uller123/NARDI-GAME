import pygame
import json

# Global constants that will be set based on screen size
BOARD_MARGIN = 30
BAR_WIDTH = 60
POINT_W = 35
POINT_H = 180
R = 12
GAP = 3


def set_board_constants(width, height):
    """Calculate board constants based on screen size"""
    global BOARD_MARGIN, BAR_WIDTH, POINT_W, POINT_H, R, GAP

    BOARD_MARGIN = int(width * 0.0375)  # ~30 for 800
    BAR_WIDTH = int(width * 0.075)  # ~60 for 800
    POINT_W = int(width * 0.04375)  # ~35 for 800
    POINT_H = int(height * 0.36)  # ~180 for 500
    R = int(min(width, height) * 0.015)  # ~12
    GAP = int(min(width, height) * 0.00375)  # ~3


# пункт → (side, column)
POINT_LAYOUT = {
    0: ("bottom", 11), 1: ("bottom", 10), 2: ("bottom", 9), 3: ("bottom", 8),
    4: ("bottom", 7), 5: ("bottom", 6), 6: ("bottom", 5), 7: ("bottom", 4),
    8: ("bottom", 3), 9: ("bottom", 2), 10: ("bottom", 1), 11: ("bottom", 0),
    12: ("top", 0), 13: ("top", 1), 14: ("top", 2), 15: ("top", 3),
    16: ("top", 4), 17: ("top", 5), 18: ("top", 6), 19: ("top", 7),
    20: ("top", 8), 21: ("top", 9), 22: ("top", 10), 23: ("top", 11),
}


def draw_board(screen, game, width, height):
    screen.fill((40, 120, 110))

    # Draw board border
    pygame.draw.rect(
        screen, (0, 0, 0),
        (BOARD_MARGIN, BOARD_MARGIN,
         width - 2 * BOARD_MARGIN,
         height - 2 * BOARD_MARGIN), 3
    )

    left = BOARD_MARGIN
    right = BOARD_MARGIN + 6 * POINT_W + BAR_WIDTH

    # Draw triangles (points)
    for idx, (side, col) in POINT_LAYOUT.items():
        x = left + col * POINT_W if col < 6 else right + (col - 6) * POINT_W

        if side == "bottom":
            y = height - BOARD_MARGIN
            pts = [(x, y), (x + POINT_W, y), (x + POINT_W // 2, y - POINT_H)]
        else:
            y = BOARD_MARGIN
            pts = [(x, y), (x + POINT_W, y), (x + POINT_W // 2, y + POINT_H)]

        color = (220, 220, 220) if idx % 2 == 0 else (180, 180, 180)
        pygame.draw.polygon(screen, color, pts)

        # Draw point number for debugging (optional)
        # font = pygame.font.SysFont(None, 20)
        # text = font.render(str(idx), True, (255, 0, 0))
        # screen.blit(text, (x + 5, height // 2))

    # Highlight possible moves - FIXED VERSION
    if game.selected is not None and game.dice:
        src = game.selected

        # Only highlight if source is an integer (not "bar")
        if isinstance(src, int):
            for d in game.dice:
                if game.turn == "White":
                    dst = src - d
                else:
                    dst = src + d

                if 0 <= dst < 24 and game.can_move(src, dst):
                    side, col = POINT_LAYOUT[dst]
                    x = (BOARD_MARGIN + col * POINT_W if col < 6
                         else BOARD_MARGIN + 6 * POINT_W + BAR_WIDTH + (col - 6) * POINT_W)
                    cx = x + POINT_W // 2
                    cy = height // 2
                    pygame.draw.circle(screen, (0, 255, 0, 100), (cx, cy), 8)

        # If selected is "bar", highlight possible entry points
        elif src == "bar" and game.bar[game.turn] > 0:
            for d in game.dice:
                if game.turn == "White":
                    # White enters from bar: need to roll 1 to enter point 23, 2 for 22, etc.
                    enter_point = 24 - d
                else:
                    # Black enters from bar: need to roll 1 to enter point 0, 2 for 1, etc.
                    enter_point = d - 1

                if 0 <= enter_point < 24:
                    # Check if point is open (fewer than 2 opponent checkers)
                    if (len(game.points[enter_point]) < 2 or
                            game.points[enter_point][-1] == game.turn):
                        side, col = POINT_LAYOUT[enter_point]
                        x = (BOARD_MARGIN + col * POINT_W if col < 6
                             else BOARD_MARGIN + 6 * POINT_W + BAR_WIDTH + (col - 6) * POINT_W)
                        cx = x + POINT_W // 2
                        cy = height // 2
                        pygame.draw.circle(screen, (0, 255, 0, 100), (cx, cy), 8)

    # Draw checkers
    for idx, stack in enumerate(game.points):
        if not stack:
            continue

        side, col = POINT_LAYOUT[idx]
        cx = (left + col * POINT_W if col < 6
              else right + (col - 6) * POINT_W) + POINT_W // 2

        for i, color in enumerate(stack):
            if side == "bottom":
                cy = height - BOARD_MARGIN - R - i * (2 * R + GAP)
            else:
                cy = BOARD_MARGIN + R + i * (2 * R + GAP)

            c = (30, 30, 30) if color == "Black" else (240, 240, 240)
            pygame.draw.circle(screen, c, (cx, cy), R)
            pygame.draw.circle(screen, (0, 0, 0), (cx, cy), R, 2)

    # Draw bar (middle)
    bar_x = left + 6 * POINT_W
    pygame.draw.rect(screen, (80, 80, 80),
                     (bar_x, BOARD_MARGIN, BAR_WIDTH, height - 2 * BOARD_MARGIN))

    # Draw checkers on bar
    for i in range(game.bar["White"]):
        cx = bar_x + BAR_WIDTH // 2
        cy = height // 2 - 20 - i * (2 * R + 5)
        pygame.draw.circle(screen, (240, 240, 240), (cx, cy), R)
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), R, 2)

    for i in range(game.bar["Black"]):
        cx = bar_x + BAR_WIDTH // 2
        cy = height // 2 + 20 + i * (2 * R + 5)
        pygame.draw.circle(screen, (30, 30, 30), (cx, cy), R)
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), R, 2)


def point_from_mouse(x, y, width, height):
    left = BOARD_MARGIN
    right = BOARD_MARGIN + 6 * POINT_W + BAR_WIDTH

    for idx, (side, col) in POINT_LAYOUT.items():
        px = left + col * POINT_W if col < 6 else right + (col - 6) * POINT_W

        if side == "bottom":
            py1 = height - BOARD_MARGIN - POINT_H
            py2 = height - BOARD_MARGIN
        else:
            py1 = BOARD_MARGIN
            py2 = BOARD_MARGIN + POINT_H

        if px <= x <= px + POINT_W and py1 <= y <= py2:
            return idx

    # Check bar area
    bar_x = left + 6 * POINT_W
    bar_y1 = BOARD_MARGIN
    bar_y2 = height - BOARD_MARGIN
    if bar_x <= x <= bar_x + BAR_WIDTH and bar_y1 <= y <= bar_y2:
        return "bar"

    return None


def draw_ui(screen, game, width, height, game_mode, moves_count):
    font = pygame.font.SysFont(None, 28)
    small_font = pygame.font.SysFont(None, 22)

    PANEL_X = width - 220
    PANEL_Y = 40

    # Game mode
    mode_text = font.render(f"Mode: {game_mode}", True, (255, 255, 255))
    screen.blit(mode_text, (PANEL_X, PANEL_Y))

    # Turn
    turn_color = (240, 240, 240) if game.turn == "White" else (30, 30, 30)
    turn_bg = (100, 100, 100) if game.turn == "White" else (200, 200, 200)
    pygame.draw.rect(screen, turn_bg, (PANEL_X, PANEL_Y + 30, 150, 30), border_radius=5)
    turn_text = font.render(f"Turn: {game.turn}", True, turn_color)
    screen.blit(turn_text, (PANEL_X + 10, PANEL_Y + 35))

    # Dice
    if game.dice:
        dice_text = font.render("Dice: " + " ".join(map(str, game.dice)), True, (255, 255, 255))
        screen.blit(dice_text, (PANEL_X, PANEL_Y + 70))
    else:
        dice_text = font.render("Press SPACE to roll", True, (255, 200, 200))
        screen.blit(dice_text, (PANEL_X, PANEL_Y + 70))

    # Off board
    off_text = font.render(f"Off: W {game.off['White']}  B {game.off['Black']}",
                           True, (255, 255, 255))
    screen.blit(off_text, (PANEL_X, PANEL_Y + 100))

    # Bar
    bar_text = font.render(f"Bar: W {game.bar['White']}  B {game.bar['Black']}",
                           True, (255, 255, 255))
    screen.blit(bar_text, (PANEL_X, PANEL_Y + 130))

    # Moves count
    moves_text = font.render(f"Moves: {moves_count}", True, (255, 255, 255))
    screen.blit(moves_text, (PANEL_X, PANEL_Y + 160))

    # Selected checker info
    if game.selected is not None:
        if game.selected == "bar":
            selected_text = font.render("Selected: Bar", True, (255, 255, 0))
        else:
            selected_text = font.render(f"Selected: Point {game.selected}", True, (255, 255, 0))
        screen.blit(selected_text, (PANEL_X, PANEL_Y + 190))

    # Instructions
    instructions = [
        "SPACE - roll dice",
        "Click - select/move",
        "S - save game",
        "L - load game",
        "ESC - back to menu"
    ]

    for i, instr in enumerate(instructions):
        instr_text = small_font.render(instr, True, (200, 200, 200))
        screen.blit(instr_text, (PANEL_X, height - 150 + i * 25))

    # Status message
    status_y = height - 30
    if game.bar[game.turn] > 0:
        status_text = font.render(f"You have {game.bar[game.turn]} checker(s) on bar!",
                                  True, (255, 100, 100))
        screen.blit(status_text, (10, status_y))
    elif game.all_in_home():
        status_text = font.render("All checkers in home! You can bear off.",
                                  True, (100, 255, 100))
        screen.blit(status_text, (10, status_y))