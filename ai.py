import random


def ai_easy(game):
    """Random AI that makes valid moves"""
    if not game.dice:
        return False

    # First, check if there are checkers on bar
    if game.bar[game.turn] > 0:
        # Try to enter from bar
        possible_entries = []
        for d in game.dice:
            if game.turn == "White":
                enter_point = 24 - d
            else:
                enter_point = d - 1

            if 0 <= enter_point < 24:
                if (len(game.points[enter_point]) < 2 or
                        game.points[enter_point][-1] == game.turn):
                    possible_entries.append(("bar", enter_point, d))

        if possible_entries:
            _, dst, die = random.choice(possible_entries)
            game.move("bar", dst)
            return True

    # Try to find all possible normal moves
    possible_moves = []
    for src in range(24):
        if game.points[src] and game.points[src][-1] == game.turn:
            for d in game.dice:
                if game.turn == "White":
                    dst = src - d
                else:
                    dst = src + d

                if 0 <= dst < 24 and game.can_move(src, dst):
                    possible_moves.append((src, dst, d))

    # Check bearing off
    if game.all_in_home():
        for src in range(24):
            if game.points[src] and game.points[src][-1] == game.turn:
                if game.can_bear_off(src):
                    for d in game.dice:
                        if game.turn == "White":
                            if src - d < 0:
                                possible_moves.append((src, -1, d))
                        else:
                            if src + d > 23:
                                possible_moves.append((src, 24, d))

    if possible_moves:
        src, dst, die = random.choice(possible_moves)
        if dst == -1 or dst == 24:
            game.bear_off(src)
        else:
            game.move(src, dst)
        return True

    # If no moves possible, skip turn
    game.turn = "White" if game.turn == "Black" else "Black"
    game.dice = []
    return False


def ai_smart(game):
    """Smarter AI that prefers certain moves"""
    if not game.dice:
        return False

    # First, check if there are checkers on bar
    if game.bar[game.turn] > 0:
        # Try to enter from bar
        possible_entries = []
        for d in game.dice:
            if game.turn == "White":
                enter_point = 24 - d
            else:
                enter_point = d - 1

            if 0 <= enter_point < 24:
                if (len(game.points[enter_point]) < 2 or
                        game.points[enter_point][-1] == game.turn):
                    weight = 50  # High priority to get off bar
                    possible_entries.append(("bar", enter_point, d, weight))

        if possible_entries:
            possible_entries.sort(key=lambda x: x[3], reverse=True)
            _, dst, die, _ = possible_entries[0]
            game.move("bar", dst)
            return True

    # Try to find all possible moves with weights
    possible_moves = []
    for src in range(24):
        if game.points[src] and game.points[src][-1] == game.turn:
            for d in game.dice:
                if game.turn == "White":
                    dst = src - d
                else:
                    dst = src + d

                if 0 <= dst < 24 and game.can_move(src, dst):
                    weight = 0

                    # Weight for hitting opponent
                    if (len(game.points[dst]) == 1 and
                            game.points[dst][-1] != game.turn):
                        weight += 40

                    # Weight for making a point (2+ checkers)
                    if len(game.points[src]) > 1 and len(game.points[dst]) == 0:
                        weight += 25

                    # Weight for moving from danger (single checker)
                    if len(game.points[src]) == 1:
                        weight += 20

                    # Weight for moving towards home
                    if game.turn == "White":
                        if dst < 6:  # Moving into home
                            weight += 15
                        elif dst < src:  # Moving left (towards home)
                            weight += 10
                    else:
                        if dst >= 18:  # Moving into home
                            weight += 15
                        elif dst > src:  # Moving right (towards home)
                            weight += 10

                    possible_moves.append((src, dst, d, weight))

    # Check bearing off
    if game.all_in_home():
        for src in range(24):
            if game.points[src] and game.points[src][-1] == game.turn:
                if game.can_bear_off(src):
                    for d in game.dice:
                        if game.turn == "White":
                            if src - d < 0:
                                weight = 60  # High priority to bear off
                                possible_moves.append((src, -1, d, weight))
                        else:
                            if src + d > 23:
                                weight = 60
                                possible_moves.append((src, 24, d, weight))

    if possible_moves:
        # Choose move with highest weight
        possible_moves.sort(key=lambda x: x[3], reverse=True)
        src, dst, die, _ = possible_moves[0]

        if dst == -1 or dst == 24:
            game.bear_off(src)
        else:
            game.move(src, dst)
        return True

    # If no moves possible, skip turn
    game.turn = "White" if game.turn == "Black" else "Black"
    game.dice = []
    return False