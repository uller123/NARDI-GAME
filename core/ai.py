import random
from core.rules import collect_moves

def ai_random_move(board, color, dice):
    moves = collect_moves(board, color, dice)
    if not moves:
        return None
    return random.choice(moves)
