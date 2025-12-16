def can_move(board, frm, to):
    if to < 0 or to >= board.size:
        return False

    if not board.points[to]:
        return True

    top = board.points[to][-1]
    cur = board.points[frm][-1]

    if top.color == cur.color:
        return True

    return len(board.points[to]) == 1


def apply_move(board, move):
    frm, to = move
    board.move_checker(frm, to)


def collect_moves(board, color, dice):
    moves = []
    for i in range(board.size):
        if board.points[i] and board.points[i][-1].color == color:
            for d in dice:
                t = i + d if color == "black" else i - d
                if can_move(board, i, t):
                    moves.append((i, t))
    return moves
