import pygame
import json
from Game import run_game
from ai import ai_easy, ai_smart

WIDTH, HEIGHT = 900, 600
FPS = 60


def draw_button(screen, text, x, y, width, height, color, hover_color, font, is_hovered):
    color_to_use = hover_color if is_hovered else color
    pygame.draw.rect(screen, color_to_use, (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2, border_radius=10)

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)


def show_game_modes(screen):
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    buttons = [
        {"text": "Player vs AI (Easy)", "rect": None, "mode": "ai_easy"},
        {"text": "Player vs AI (Smart)", "rect": None, "mode": "ai_smart"},
        {"text": "Hot Seat (2 Players)", "rect": None, "mode": "hotseat"},
        {"text": "Back", "rect": None, "mode": "back"}
    ]

    while True:
        screen.fill((30, 30, 30))

        # Title
        title = title_font.render("Select Game Mode", True, (240, 240, 240))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw buttons
        for i, button in enumerate(buttons):
            x = WIDTH // 2 - 150
            y = 150 + i * 80
            is_hovered = button["rect"] and button["rect"].collidepoint(pygame.mouse.get_pos())
            rect = draw_button(screen, button["text"], x, y, 300, 60,
                               (70, 70, 120), (100, 100, 160), font, is_hovered)
            button["rect"] = rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"] and button["rect"].collidepoint(event.pos):
                        if button["mode"] == "back":
                            return "back"
                        else:
                            return button["mode"]

        pygame.display.flip()
        clock.tick(FPS)


def show_board_size(screen):
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    sizes = [
        {"name": "Small (800x500)", "size": (800, 500)},
        {"name": "Medium (1000x600)", "size": (1000, 600)},
        {"name": "Large (1200x700)", "size": (1200, 700)},
        {"name": "Back", "size": None}
    ]

    buttons = []
    for i, size in enumerate(sizes):
        buttons.append({"text": size["name"], "rect": None, "size": size["size"]})

    while True:
        screen.fill((30, 30, 30))

        # Title
        title = title_font.render("Select Board Size", True, (240, 240, 240))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw buttons
        for i, button in enumerate(buttons):
            x = WIDTH // 2 - 150
            y = 150 + i * 80
            is_hovered = button["rect"] and button["rect"].collidepoint(pygame.mouse.get_pos())
            rect = draw_button(screen, button["text"], x, y, 300, 60,
                               (70, 120, 70), (100, 160, 100), font, is_hovered)
            button["rect"] = rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"] and button["rect"].collidepoint(event.pos):
                        if button["size"] is None:
                            return "back"
                        else:
                            return button["size"]

        pygame.display.flip()
        clock.tick(FPS)


def show_high_scores(screen):
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    try:
        with open("highscores.json", "r") as f:
            scores = json.load(f)
    except:
        scores = []

    while True:
        screen.fill((30, 30, 30))

        # Title
        title = title_font.render("High Scores", True, (240, 240, 240))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Display scores
        y = 120
        if not scores:
            no_scores = font.render("No scores yet!", True, (200, 200, 200))
            screen.blit(no_scores, (WIDTH // 2 - no_scores.get_width() // 2, y))
        else:
            for i, score in enumerate(scores[:10]):  # Top 10
                score_text = f"{i + 1}. {score['winner']} vs {score['loser']} - {score['moves']} moves"
                score_surf = font.render(score_text, True, (240, 240, 240))
                screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, y + i * 40))

        # Back button
        back_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)
        is_hovered = back_rect.collidepoint(pygame.mouse.get_pos())
        draw_button(screen, "Back", back_rect.x, back_rect.y, back_rect.width, back_rect.height,
                    (120, 70, 70), (160, 100, 100), font, is_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return True

        pygame.display.flip()
        clock.tick(FPS)


def main_menu():
    pygame.display.set_caption("Nardi")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()

    buttons = [
        {"text": "Start Game", "rect": None},
        {"text": "High Scores", "rect": None},
        {"text": "Quit", "rect": None}
    ]

    while True:
        screen.fill((30, 30, 30))

        # Title
        title = title_font.render("NARDI", True, (240, 240, 240))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # Draw buttons
        for i, button in enumerate(buttons):
            x = WIDTH // 2 - 100
            y = 200 + i * 80
            is_hovered = button["rect"] and button["rect"].collidepoint(pygame.mouse.get_pos())
            rect = draw_button(screen, button["text"], x, y, 200, 60,
                               (70, 70, 120), (100, 100, 160), font, is_hovered)
            button["rect"] = rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button["rect"] and button["rect"].collidepoint(event.pos):
                        if i == 0:  # Start Game
                            while True:
                                mode = show_game_modes(screen)
                                if mode is None:
                                    return
                                if mode == "back":
                                    break

                                size = show_board_size(screen)
                                if size is None:
                                    return
                                if size == "back":
                                    continue

                                # Start game with selected mode and size
                                run_game(screen, mode, size)
                                break

                        elif i == 1:  # High Scores
                            show_high_scores(screen)

                        elif i == 2:  # Quit
                            return

        pygame.display.flip()
        clock.tick(FPS)