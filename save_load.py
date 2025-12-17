import json

SAVE_FILE = "save.json"

def save_game(game):
    data = {
        "points": game.points,
        "turn": game.turn,
        "dice": game.dice
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_game(game):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    game.points = data["points"]
    game.turn = data["turn"]
    game.dice = data["dice"]
