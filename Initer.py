from Game import *


def init_bases(game_state):
    Base(game_state, 550, 0, 0, "Down")

    for i in range(6):
        Base(game_state, 505 - 37 * i, 510, i + 1, "Up")
    for i in range(6):
        Base(game_state, 247 - 37 * i, 510, 7 + i, "Up")
    for i in range(6):
        Base(game_state, 60 + 37 * i, 60, 13 + i, "Down")
    for i in range(6):
        Base(game_state, 320 + 37 * i, 60, 19 + i, "Down")
    for i in range(2):
        game_state.baseList[1].add_washer(Washer("Black", 505, 510 - 50 * i, game_state.baseList[1], i))
        game_state.baseList[24].add_washer(Washer("White", 320 + 37 * 5, 60 + 50 * i, game_state.baseList[24], i))
    for i in range(5):
        game_state.baseList[6].add_washer(Washer("White", 505 - 37 * 5, 510 - 50 * i, game_state.baseList[6], i))
        game_state.baseList[19].add_washer(Washer("Black", 320, 60 + 50 * i, game_state.baseList[19], i))
        game_state.baseList[12].add_washer(Washer("Black", 247 - 37 * 5, 510 - 50 * i, game_state.baseList[12], i))
        game_state.baseList[13].add_washer(Washer("White", 60, 60 + 50 * i, game_state.baseList[13], i))
    for i in range(3):
        game_state.baseList[8].add_washer(Washer("White", 247 - 37, 510 - 50 * i, game_state.baseList[8], i))
        game_state.baseList[17].add_washer(Washer("Black", 60 + 37 * 4, 60 + 50 * i, game_state.baseList[17], i))
    Base(game_state, 0, 50, 25, "Down")