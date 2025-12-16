import random

class Dice:
    def roll(self):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        if a == b:
            return [a] * 4
        return [a, b]
