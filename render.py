import pygame


WIDTH, HEIGHT = 800, 500

BOARD_MARGIN = 30
BAR_WIDTH = 60

POINT_W = 35
POINT_H = 180

R = 12
GAP = 3

# пункт → (side, column)
# side: "bottom" / "top"
POINT_LAYOUT = {
    # низ: справа → влево (1–12)
    0:  ("bottom", 11),
    1:  ("bottom", 10),
    2:  ("bottom", 9),
    3:  ("bottom", 8),
    4:  ("bottom", 7),
    5:  ("bottom", 6),
    6:  ("bottom", 5),
    7:  ("bottom", 4),
    8:  ("bottom", 3),
    9:  ("bottom", 2),
    10: ("bottom", 1),
    11: ("bottom", 0),

    # верх: слева → вправо (13–24)
    12: ("top", 0),
    13: ("top", 1),
    14: ("top", 2),
    15: ("top", 3),
    16: ("top", 4),
    17: ("top", 5),
    18: ("top", 6),
    19: ("top", 7),
    20: ("top", 8),
    21: ("top", 9),
    22: ("top", 10),
    23: ("top", 11),
}


def draw_board(screen, game):
    screen.fill((40, 120, 110))

    pygame.draw.rect(
        screen, (0, 0, 0),
        (BOARD_MARGIN, BOARD_MARGIN,
         WIDTH - 2 * BOARD_MARGIN,
         HEIGHT - 2 * BOARD_MARGIN), 3
    )

    left = BOARD_MARGIN
    right = BOARD_MARGIN + 6 * POINT_W + BAR_WIDTH

    # --- треугольники ---
    for idx, (side, col) in POINT_LAYOUT.items():
        x = left + col * POINT_W if col < 6 else right + (col - 6) * POINT_W

        if side == "bottom":
            y = HEIGHT - BOARD_MARGIN
            pts = [(x, y), (x + POINT_W, y), (x + POINT_W // 2, y - POINT_H)]
        else:
            y = BOARD_MARGIN
            pts = [(x, y), (x + POINT_W, y), (x + POINT_W // 2, y + POINT_H)]

        color = (220, 220, 220) if idx % 2 == 0 else (180, 180, 180)
        pygame.draw.polygon(screen, color, pts)
    
    # подсветка возможных ходов
    if game.selected is not None and game.dice:
        src = game.selected
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
                cy = HEIGHT // 2
                pygame.draw.circle(screen, (0, 255, 0), (cx, cy), 6)

    # --- шашки ---
    for idx, stack in enumerate(game.points):
        if not stack:
            continue

        side, col = POINT_LAYOUT[idx]
        cx = (left + col * POINT_W if col < 6 else right + (col - 6) * POINT_W) + POINT_W // 2

        for i, color in enumerate(stack):
            if side == "bottom":
                cy = HEIGHT - BOARD_MARGIN - R - i * (2 * R + GAP)
            else:
                cy = BOARD_MARGIN + R + i * (2 * R + GAP)

            c = (30, 30, 30) if color == "Black" else (240, 240, 240)
            pygame.draw.circle(screen, c, (cx, cy), R)
            pygame.draw.circle(screen, (0, 0, 0), (cx, cy), R, 2)

def point_from_mouse(x, y):
    left = BOARD_MARGIN
    right = BOARD_MARGIN + 6 * POINT_W + BAR_WIDTH

    for idx, (side, col) in POINT_LAYOUT.items():
        px = left + col * POINT_W if col < 6 else right + (col - 6) * POINT_W

        if side == "bottom":
            py1 = HEIGHT - BOARD_MARGIN - POINT_H
            py2 = HEIGHT - BOARD_MARGIN
        else:
            py1 = BOARD_MARGIN
            py2 = BOARD_MARGIN + POINT_H

        if px <= x <= px + POINT_W and py1 <= y <= py2:
            return idx
    return None

def draw_ui(screen, game):
    font = pygame.font.SysFont(None, 28)  # ← ВОТ ЭТОГО НЕ ХВАТАЛО

    PANEL_X = WIDTH - 220   # правая панель
    PANEL_Y = 40

    # чей ход
    turn_text = font.render(f"Turn: {game.turn}", True, (255, 255, 255))
    screen.blit(turn_text, (PANEL_X, PANEL_Y))


    if game.dice:
        dice_text = font.render(
            "Dice: " + " ".join(map(str, game.dice)),
            True, (255, 255, 255)
        )
    else:
        dice_text = font.render("Press SPACE", True, (255, 200, 200))

    screen.blit(dice_text, (PANEL_X, PANEL_Y + 40))

    off_text = font.render(
    f"Off: W {game.off['White']}  B {game.off['Black']}",
    True, (255, 255, 255)
    )
    screen.blit(off_text, (PANEL_X, PANEL_Y + 80))

