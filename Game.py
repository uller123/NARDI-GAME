import pygame
import random
import sys
from render import draw_board, point_from_mouse, draw_ui, set_board_constants, check_bear_off_click
from save_load import save_game, load_game, save_highscore
from ai import ai_easy, ai_smart


class GameState:
    def __init__(self, width, height):
        self.points = [[] for _ in range(24)]   # пункты доски
        self.turn = "White"                     # текущий ход
        self.dice = []                          # кубики
        self.selected = None                    # выбранная шашка
        self.bar = {"White": 0, "Black": 0}     # выбитые шашки
        self.off = {"White": 0, "Black": 0}     # вынесенные шашки
        self.width = width
        self.height = height
        self._init_position()

    def _init_position(self):
        """Начальная расстановка шашек"""
        self.points[0] = ["Black"] * 2
        self.points[5] = ["White"] * 5
        self.points[7] = ["White"] * 3
        self.points[11] = ["Black"] * 5
        self.points[12] = ["White"] * 5
        self.points[16] = ["Black"] * 3
        self.points[18] = ["Black"] * 5
        self.points[23] = ["White"] * 2

    def roll_dice(self):
        """Бросок кубиков"""
        if not self.dice:
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            self.dice = [d1, d2] if d1 != d2 else [d1] * 4
        return self.dice

    def can_move(self, src, dst):
        """Проверка допустимости хода"""
        if not self.dice:
            return False

        # вход с бара
        if src == "bar":
            if self.bar[self.turn] == 0:
                return False

            needed = 24 - dst if self.turn == "White" else dst + 1
            if needed not in self.dice:
                return False

            if len(self.points[dst]) >= 2 and self.points[dst][-1] != self.turn:
                return False

            return True

        # обычный ход
        if dst < 0 or dst >= 24:
            return False
        if not self.points[src] or self.points[src][-1] != self.turn:
            return False
        if self.bar[self.turn] > 0:
            return False

        dist = src - dst if self.turn == "White" else dst - src
        if dist <= 0 or dist not in self.dice:
            return False

        if len(self.points[dst]) >= 2 and self.points[dst][-1] != self.turn:
            return False

        return True

    def move(self, src, dst):
        """Выполнение хода"""
        if src == "bar":
            needed = 24 - dst if self.turn == "White" else dst + 1
            if needed not in self.dice:
                return
            self.dice.remove(needed)
            self.bar[self.turn] -= 1
        else:
            dist = src - dst if self.turn == "White" else dst - src
            if dist not in self.dice:
                return
            self.dice.remove(dist)
            self.points[src].pop()

        # выбивание
        if len(self.points[dst]) == 1 and self.points[dst][-1] != self.turn:
            hit = self.points[dst].pop()
            self.bar[hit] += 1

        self.points[dst].append(self.turn)

        if not self.dice:
            self.turn = "Black" if self.turn == "White" else "White"

    def all_in_home(self):
        """Все ли шашки в доме"""
        home = range(0, 6) if self.turn == "White" else range(18, 24)
        if self.bar[self.turn] > 0:
            return False
        for i in range(24):
            if i not in home and self.points[i] and self.points[i][-1] == self.turn:
                return False
        return True

    def can_bear_off(self, src):
        """Можно ли вынести шашку"""
        if not self.all_in_home():
            return False
        if not self.points[src] or self.points[src][-1] != self.turn:
            return False

        need = src + 1 if self.turn == "White" else 24 - src
        return any(d >= need for d in self.dice)

    def bear_off(self, src):
        """Вынос шашки"""
        need = src + 1 if self.turn == "White" else 24 - src
        usable = [d for d in self.dice if d >= need]
        if not usable:
            return False

        self.dice.remove(min(usable))
        self.points[src].pop()
        self.off[self.turn] += 1

        if not self.dice:
            self.turn = "Black" if self.turn == "White" else "White"
        return True

    def has_any_move(self):
        """Есть ли хоть один ход"""
        if self.bar[self.turn] > 0:
            for d in self.dice:
                dst = 24 - d if self.turn == "White" else d - 1
                if 0 <= dst < 24:
                    if len(self.points[dst]) < 2 or self.points[dst][-1] == self.turn:
                        return True
            return False

        for src in range(24):
            if self.points[src] and self.points[src][-1] == self.turn:
                for d in self.dice:
                    dst = src - d if self.turn == "White" else src + d
                    if 0 <= dst < 24 and self.can_move(src, dst):
                        return True

        if self.all_in_home():
            for src in range(24):
                if self.can_bear_off(src):
                    return True

        return False

    def check_win(self):
        """Проверка победы"""
        if self.off["White"] == 15:
            return "White"
        if self.off["Black"] == 15:
            return "Black"
        return None


    def calculate_score(self):
        # Simple scoring: winner gets 1 point per checker left on opponent's board
        if self.off["White"] == 15:
            black_left = sum(len(p) for p in self.points if any(c == "Black" for c in p))
            return 1 + black_left // 5  # Bonus for gammon/backgammon
        elif self.off["Black"] == 15:
            white_left = sum(len(p) for p in self.points if any(c == "White" for c in p))
            return 1 + white_left // 5
        return 0


def show_game_over(screen, winner, moves_count, width, height):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    # Winner text
    winner_text = font.render(f"{winner} Wins!", True,
                              (240, 240, 240) if winner == "White" else (30, 30, 30))
    screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 - 50))

    # Moves count
    moves_text = small_font.render(f"Moves: {moves_count}", True, (200, 200, 200))
    screen.blit(moves_text, (width // 2 - moves_text.get_width() // 2, height // 2))

    # Continue text
    continue_text = small_font.render("Press any key to continue...", True, (200, 200, 200))
    screen.blit(continue_text, (width // 2 - continue_text.get_width() // 2, height // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def run_game(screen, game_mode, size):
    width, height = size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Nardi - {game_mode}")

    set_board_constants(width, height)
    clock = pygame.time.Clock()
    game = GameState(width, height)

    moves_count = 0
    ai_thinking = False
    ai_delay = 30  # Frames to wait for AI move
    ai_delay_counter = 0

    # Initial dice roll for white if playing against AI
    if game_mode.startswith("ai"):
        game.roll_dice()
        moves_count += 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Human player rolls dice
                if event.key == pygame.K_SPACE and not ai_thinking:
                    if (game_mode == "hotseat" or
                            (game_mode.startswith("ai") and game.turn == "White")):
                        if not game.dice:  # Only roll if dice are empty
                            game.roll_dice()
                            moves_count += 1

                            # Check if player has any moves
                            if not game.has_any_move():
                                print(f"No moves available. Turn passed to {game.turn}")
                                game.turn = "Black" if game.turn == "White" else "White"
                                game.dice = []
                        else:
                            print(f"Dice already rolled: {game.dice}")

                if event.key == pygame.K_s:
                    save_game(game, moves_count)
                    print("Game saved!")

                if event.key == pygame.K_l:
                    moves_count = load_game(game)
                    print("Game loaded!")
                    # Reset AI thinking state
                    ai_thinking = False
                    ai_delay_counter = 0

            # Handle mouse clicks for human players
            if (event.type == pygame.MOUSEBUTTONDOWN and
                    not ai_thinking and
                    (game_mode == "hotseat" or
                     (game_mode.startswith("ai") and game.turn == "White"))):

                mx, my = pygame.mouse.get_pos()

                # First check for bear off click
                bear_off_click = check_bear_off_click(mx, my, width, height, game)
                if bear_off_click and game.selected is not None and isinstance(game.selected, int):
                    # Try to bear off the selected checker
                    if game.can_bear_off(game.selected):
                        if game.bear_off(game.selected):
                            game.selected = None

                            # Check for win
                            win = game.check_win()
                            if win:
                                # Calculate scores
                                winner_score = game.calculate_score()
                                loser_score = 1

                                # Save to high scores
                                loser = "Black" if win == "White" else "White"
                                save_highscore(win, loser, moves_count, winner_score, loser_score)

                                show_game_over(screen, win, moves_count, width, height)
                                running = False
                    else:
                        print(f"Cannot bear off from point {game.selected}")
                    continue

                # Normal point/bar click
                idx = point_from_mouse(mx, my, width, height)

                if idx is None:
                    game.selected = None
                    continue

                if game.selected is None:
                    # Select checker or bar
                    if idx == "bar":
                        if game.bar[game.turn] > 0:
                            game.selected = "bar"
                            print(f"Selected bar ({game.turn} on bar)")
                    elif (game.points[idx] and
                          game.points[idx][-1] == game.turn):
                        game.selected = idx
                        print(f"Selected point {idx}")
                    else:
                        print(f"Cannot select point {idx} - not your checker")

                else:
                    # Try to move
                    if idx == "bar":
                        game.selected = None
                        print("Deselected (clicked bar)")
                    elif game.selected == "bar":
                        # Move from bar
                        if game.can_move("bar", idx):
                            game.move("bar", idx)
                            game.selected = None

                            # Check for win
                            win = game.check_win()
                            if win:
                                # Calculate scores
                                winner_score = game.calculate_score()
                                loser_score = 1

                                # Save to high scores
                                loser = "Black" if win == "White" else "White"
                                save_highscore(win, loser, moves_count, winner_score, loser_score)

                                show_game_over(screen, win, moves_count, width, height)
                                running = False
                        else:
                            print(f"Cannot move from bar to {idx}")
                            game.selected = None
                    elif game.can_move(game.selected, idx):
                        # Normal move
                        game.move(game.selected, idx)
                        game.selected = None

                        # Check for win
                        win = game.check_win()
                        if win:
                            # Calculate scores
                            winner_score = game.calculate_score()
                            loser_score = 1

                            # Save to high scores
                            loser = "Black" if win == "White" else "White"
                            save_highscore(win, loser, moves_count, winner_score, loser_score)

                            show_game_over(screen, win, moves_count, width, height)
                            running = False
                    else:
                        # Try to select different checker
                        if idx == "bar":
                            if game.bar[game.turn] > 0:
                                game.selected = "bar"
                                print(f"Selected bar")
                        elif (game.points[idx] and
                              game.points[idx][-1] == game.turn):
                            game.selected = idx
                            print(f"Selected point {idx}")
                        else:
                            game.selected = None
                            print(f"Deselected (cannot move to {idx})")

        if game_mode.startswith("ai") and game.turn == "Black" and not ai_thinking and running:
            if not game.dice:
                # AI needs to roll dice
                print("AI rolling dice...")
                game.roll_dice()
                moves_count += 1

                # Check if AI has any moves
                if not game.has_any_move():
                    print("AI has no moves. Passing turn.")
                    game.turn = "White"
                    game.dice = []
                else:
                    # Start AI thinking
                    ai_thinking = True
                    ai_delay_counter = 0
            elif game.dice:
                # AI has dice, start thinking
                ai_thinking = True
                ai_delay_counter = 0

        # AI thinking process
        if ai_thinking and running:
            ai_delay_counter += 1

            if ai_delay_counter >= ai_delay:
                ai_delay_counter = 0

                # AI makes a move
                moved = False
                if game_mode == "ai_easy":
                    moved = ai_easy(game)
                else:  # ai_smart
                    moved = ai_smart(game)

                if moved:
                    print(f"AI moved. Remaining dice: {game.dice}")

                    # Check for win
                    win = game.check_win()
                    if win:
                        # Calculate scores
                        winner_score = game.calculate_score()
                        loser_score = 1

                        # Save to high scores
                        loser = "Black" if win == "White" else "White"
                        save_highscore(win, loser, moves_count, winner_score, loser_score)

                        show_game_over(screen, win, moves_count, width, height)
                        running = False
                        ai_thinking = False

                    # If dice are empty after move, AI is done
                    if not game.dice:
                        print("AI finished all moves.")
                        ai_thinking = False
                    # If dice still remain and AI can move, continue
                    elif game.has_any_move():
                        print("AI continues thinking...")
                    else:
                        print("AI cannot move with remaining dice.")
                        ai_thinking = False
                else:
                    # AI cannot make a move
                    print("AI cannot make a move. Passing turn.")
                    game.turn = "White"
                    game.dice = []
                    ai_thinking = False

        # Draw everything
        draw_board(screen, game, width, height)
        draw_ui(screen, game, width, height, game_mode, moves_count)

        # Show AI thinking
        if ai_thinking:
            font = pygame.font.SysFont(None, 36)
            thinking = font.render("AI Thinking...", True, (255, 255, 0))
            screen.blit(thinking, (width // 2 - thinking.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)

    return True