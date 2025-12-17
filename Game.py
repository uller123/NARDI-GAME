import pygame
import random
import sys
from render import draw_board, point_from_mouse, draw_ui, set_board_constants
from save_load import save_game, load_game, save_highscore
from ai import ai_easy, ai_smart


class GameState:
    def __init__(self, width, height):
        self.points = [[] for _ in range(24)]
        self.turn = "White"
        self.dice = []
        self.selected = None
        self.bar = {"White": 0, "Black": 0}
        self.off = {"White": 0, "Black": 0}
        self.width = width
        self.height = height
        self._init_position()

    def _init_position(self):
        # Standard backgammon setup
        self.points[0] = ["Black"] * 2
        self.points[5] = ["White"] * 5
        self.points[7] = ["White"] * 3
        self.points[11] = ["Black"] * 5
        self.points[12] = ["White"] * 5
        self.points[16] = ["Black"] * 3
        self.points[18] = ["Black"] * 5
        self.points[23] = ["White"] * 2

    def roll_dice(self):
        if not self.dice:  # Only roll if dice are empty
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            self.dice = [d1, d2] if d1 != d2 else [d1] * 4
            print(f"Dice rolled: {self.dice}")
        return self.dice

    def can_move(self, src, dst):
        if not self.dice:
            return False

        # If checker is on bar
        if src == "bar":
            if self.bar[self.turn] == 0:
                return False

            # Check if can enter from bar
            if self.turn == "White":
                # White enters from bar: need to roll 1 to enter point 23, 2 for 22, etc.
                needed_die = 24 - dst if 0 <= dst < 24 else None
                if needed_die is None:
                    return False
                # Check if point is blocked (2+ opponent checkers)
                if len(self.points[dst]) >= 2 and self.points[dst][-1] != self.turn:
                    return False
                return needed_die in self.dice
            else:
                # Black enters from bar: need to roll 1 to enter point 0, 2 for 1, etc.
                needed_die = dst + 1 if 0 <= dst < 24 else None
                if needed_die is None:
                    return False
                if len(self.points[dst]) >= 2 and self.points[dst][-1] != self.turn:
                    return False
                return needed_die in self.dice

        # Normal move
        if dst < 0 or dst >= 24:
            return False
        if not self.points[src]:
            return False
        if self.points[src][-1] != self.turn:
            return False

        # Check if any checkers on bar
        if self.bar[self.turn] > 0:
            return False

        if self.turn == "White":
            dist = src - dst
        else:
            dist = dst - src

        if dist <= 0 or dist not in self.dice:
            return False

        # Check if destination is blocked
        if len(self.points[dst]) >= 2 and self.points[dst][-1] != self.turn:
            return False

        return True

    def can_bear_off(self, src):
        if not self.all_in_home():
            return False

        if not self.points[src]:
            return False

        if self.points[src][-1] != self.turn:
            return False

        # Check if exact roll needed
        if self.turn == "White":
            if src + 1 in self.dice:  # Need exact roll to bear off from farthest point
                return True
            # Can bear off with higher roll if no checkers behind
            for i in range(src + 1, 6):
                if self.points[i] and self.points[i][-1] == self.turn:
                    return False
            return any(d > src for d in self.dice)
        else:
            if (24 - src) in self.dice:
                return True
            for i in range(18, src):
                if self.points[i] and self.points[i][-1] == self.turn:
                    return False
            return any(d > (24 - src) for d in self.dice)

    def bear_off(self, src):
        if self.turn == "White":
            dist = src + 1
        else:
            dist = 24 - src

        # Find the smallest die that's >= needed distance
        usable_dice = [d for d in self.dice if d >= dist]
        if not usable_dice:
            return False

        die_to_use = min(usable_dice)
        self.dice.remove(die_to_use)
        self.points[src].pop()
        self.off[self.turn] += 1

        if not self.dice:
            self.turn = "Black" if self.turn == "White" else "Black"

        return True

    def move(self, src, dst):
        print(f"Moving from {src} to {dst}")

        if src == "bar":
            # Enter from bar
            if self.turn == "White":
                # For white: point 23 needs die 1, point 22 needs die 2, etc.
                needed_die = 24 - dst
            else:
                # For black: point 0 needs die 1, point 1 needs die 2, etc.
                needed_die = dst + 1

            print(f"Need die {needed_die} to enter from bar to point {dst}")

            # Make sure the die is in dice
            if needed_die in self.dice:
                self.dice.remove(needed_die)
            else:
                print(f"Error: Die {needed_die} not in dice {self.dice}")
                return

            self.bar[self.turn] -= 1

            # Hit opponent if single checker
            if len(self.points[dst]) == 1 and self.points[dst][-1] != self.turn:
                hit_color = self.points[dst].pop()
                self.bar[hit_color] += 1

            self.points[dst].append(self.turn)

        else:
            # Normal move
            if self.turn == "White":
                dist = src - dst
            else:
                dist = dst - src

            # Make sure the die is in dice
            if dist in self.dice:
                self.dice.remove(dist)
            else:
                print(f"Error: Die {dist} not in dice {self.dice}")
                return

            # Hit opponent
            if len(self.points[dst]) == 1 and self.points[dst][-1] != self.turn:
                hit_color = self.points[dst].pop()
                self.bar[hit_color] += 1

            self.points[dst].append(self.points[src].pop())

        if not self.dice:
            self.turn = "Black" if self.turn == "White" else "White"
            print(f"Turn switched to: {self.turn}")

    def all_in_home(self):
        if self.turn == "White":
            home_range = range(0, 6)
        else:
            home_range = range(18, 24)

        # Check if any checkers on bar
        if self.bar[self.turn] > 0:
            return False

        # Check if all checkers in home quadrant
        for i in range(24):
            if i not in home_range and self.points[i] and self.points[i][-1] == self.turn:
                return False

        return True

    def has_any_move(self):
        # Check moves from bar
        if self.bar[self.turn] > 0:
            for d in self.dice:
                if self.turn == "White":
                    # White can enter from bar to point (24 - d)
                    enter_point = 24 - d
                else:
                    # Black can enter from bar to point (d - 1)
                    enter_point = d - 1

                if 0 <= enter_point < 24:
                    # Check if point is open (fewer than 2 opponent checkers)
                    if (len(self.points[enter_point]) < 2 or
                            self.points[enter_point][-1] == self.turn):
                        return True
            return False

        # Check normal moves
        for src in range(24):
            if self.points[src] and self.points[src][-1] == self.turn:
                for d in self.dice:
                    if self.turn == "White":
                        dst = src - d
                    else:
                        dst = src + d

                    if 0 <= dst < 24 and self.can_move(src, dst):
                        return True

        # Check bearing off
        if self.all_in_home():
            for src in range(24):
                if self.points[src] and self.points[src][-1] == self.turn:
                    if self.can_bear_off(src):
                        return True

        return False

    def check_win(self):
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
    ai_needs_to_roll = False

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
                    ai_needs_to_roll = False

            # Handle mouse clicks for human players
            if (event.type == pygame.MOUSEBUTTONDOWN and
                    not ai_thinking and
                    (game_mode == "hotseat" or
                     (game_mode.startswith("ai") and game.turn == "White"))):

                mx, my = pygame.mouse.get_pos()
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

        # AI move logic - COMPLETELY REWRITTEN
        if game_mode.startswith("ai") and game.turn == "Black" and not ai_thinking and running:
            if not game.dice:
                # AI needs to roll dice first
                print("AI needs to roll dice...")
                ai_needs_to_roll = True
                ai_thinking = True
                ai_delay_counter = 0
            elif game.dice:
                # AI has dice and should make moves
                print("AI starting to think with dice...")
                ai_needs_to_roll = False
                ai_thinking = True
                ai_delay_counter = 0

        # AI thinking process
        if ai_thinking and running:
            ai_delay_counter += 1

            if ai_delay_counter >= ai_delay:
                ai_delay_counter = 0

                if ai_needs_to_roll:
                    # Roll dice for AI
                    game.roll_dice()
                    moves_count += 1
                    ai_needs_to_roll = False

                    # Check if AI has any moves
                    if not game.has_any_move():
                        print("AI has no moves after rolling. Passing turn.")
                        game.turn = "White"
                        game.dice = []
                        ai_thinking = False
                    else:
                        print(f"AI rolled dice: {game.dice}")
                        # AI will make moves on next frame

                elif game.dice:
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
                        # If dice still remain, AI will continue on next frame

                    else:
                        # AI cannot make a move
                        print("AI cannot make a move. Passing turn.")
                        game.turn = "White"
                        game.dice = []
                        ai_thinking = False

                else:
                    # No dice, AI should be done
                    ai_thinking = False

        # Draw everything
        draw_board(screen, game, width, height)
        draw_ui(screen, game, width, height, game_mode, moves_count)

        # Show AI thinking
        if ai_thinking:
            font = pygame.font.SysFont(None, 36)
            if ai_needs_to_roll:
                thinking = font.render("AI Rolling Dice...", True, (255, 255, 0))
            else:
                thinking = font.render("AI Thinking...", True, (255, 255, 0))
            screen.blit(thinking, (width // 2 - thinking.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)

    return True