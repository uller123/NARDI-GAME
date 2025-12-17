import pygame
import random
from render import draw_board, point_from_mouse, draw_ui
from save_load import save_game, load_game




class GameState:
    def __init__(self):
        self.points = [[] for _ in range(24)]
        self.turn = "White"
        self.dice = []
        self.selected = None
        self._init_position()
        self.off = {"White": 0, "Black": 0}


    def _init_position(self):
        self.points[0]  = ["Black"] * 2
        self.points[5]  = ["White"] * 5
        self.points[7]  = ["White"] * 3
        self.points[11] = ["Black"] * 5
        self.points[12] = ["White"] * 5
        self.points[16] = ["Black"] * 3
        self.points[18] = ["Black"] * 5
        self.points[23] = ["White"] * 2

    # -------- ЛОГИКА --------

    def roll_dice(self):
        d1, d2 = random.randint(1,6), random.randint(1,6)
        self.dice = [d1, d2] if d1 != d2 else [d1]*4

    def can_move(self, src, dst):
        if not self.dice:
            return False
        if dst < 0 or dst >= 24:
            return False

        if not self.points[src]:
            return False

        if self.points[src][-1] != self.turn:
            return False

        if self.turn == "White":
            dist = src - dst      # белые идут ВЛЕВО
        else:
            dist = dst - src      # чёрные идут ВПРАВО

        if dist <= 0 or dist not in self.dice:
            return False
        if self.all_in_home():
            if self.turn == "White" and dst < 0:
                return True
            if self.turn == "Black" and dst > 23:
                return True

    # ---- обычный ход ----
        if dst < 0 or dst > 23:
            return False


        # проверка занятости
        if len(self.points[dst]) >= 2 and self.points[dst][-1] != self.turn:
            return False

        return True

    def move(self, src, dst):
        if self.turn == "White":
            dist = src - dst
        else:
            dist = dst - src

        # вынос шашки
        if self.all_in_home():
            if self.turn == "White" and dst < 0:
                self.points[src].pop()
                self.off["White"] += 1
                self.dice.remove(dist)
                if not self.dice:
                    self.turn = "Black"
                return

            if self.turn == "Black" and dst > 23:
                self.points[src].pop()
                self.off["Black"] += 1
                self.dice.remove(dist)
                if not self.dice:
                    self.turn = "White"
                return


        self.dice.remove(dist)


        # удар
        if len(self.points[dst]) == 1 and self.points[dst][-1] != self.turn:
            self.points[dst].pop()

        self.points[dst].append(self.points[src].pop())

        if not self.dice:
            self.turn = "Black" if self.turn == "White" else "White"

    def check_win(self):
        if self.off["White"] == 15:
            return "White"
        if self.off["Black"] == 15:
            return "Black"
        return None
  
      
    def has_any_move(self):
        for i in range(24):
            if self.points[i] and self.points[i][-1] == self.turn:
                for d in self.dice:
                    if self.turn == "White":
                        dst = i - d
                    else:
                        dst = i + d

                    if 0 <= dst < 24 and self.can_move(i, dst):
                        return True
        return False
    
    def all_in_home(self):
        if self.turn == "White":
            home_range = range(0, 6)
        else:
            home_range = range(18, 24)

        total = sum(p.count(self.turn) for p in self.points)
        home = sum(self.points[i].count(self.turn) for i in home_range)

        return total == home



def run_game(screen):
    clock = pygame.time.Clock()
    game = GameState()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.roll_dice()

                    if not game.has_any_move():
                        game.turn = "Black" if game.turn == "White" else "White"
                        game.dice = []


            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                idx = point_from_mouse(mx, my)
                if idx is None:
                    continue

                if game.selected is None:
                    game.selected = idx
                else:
                    if game.can_move(game.selected, idx):
                        game.move(game.selected, idx)
                    game.selected = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.roll_dice()
                    if not game.has_any_move():
                        game.turn = "Black" if game.turn == "White" else "White"
                        game.dice = []

                if event.key == pygame.K_s:
                    save_game(game)

                if event.key == pygame.K_l:
                    load_game(game)


        draw_board(screen, game)

        win = game.check_win()
        if win:
            pygame.display.set_caption(f"{win} wins!")
        draw_ui(screen, game)

        pygame.display.flip()
        clock.tick(60)
