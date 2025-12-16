from core.checker import Checker
from core.rules import can_move

class Board:
    def __init__(self, size):
        self.size = size
        self.points = [[] for _ in range(size)]
        self.setup()

    def setup(self):
        for _ in range(2):
            self.points[0].append(Checker("black", 0))
            self.points[-1].append(Checker("white", self.size - 1))

    def move_checker(self, frm, to):
        checker = self.points[frm].pop()
        checker.pos = to
        self.points[to].append(checker)

    def pick_move(self, mx, my, color, step):
        idx = mx // 30
        if 0 <= idx < self.size and self.points[idx]:
            checker = self.points[idx][-1]
            if checker.color == color:
                target = idx + step if color == "black" else idx - step
                if can_move(self, idx, target):
                    return (idx, target)
        return None
