import json
import os

SAVE_FILE = "save.json"
HIGHSCORES_FILE = "highscores.json"


def save_game(game, moves_count):
    data = {
        "points": game.points,
        "turn": game.turn,
        "dice": game.dice,
        "bar": game.bar,
        "off": game.off,
        "moves_count": moves_count,
        "selected": game.selected
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, default=lambda x: str(x) if x == "bar" else x)


def load_game(game):
    if not os.path.exists(SAVE_FILE):
        print("No save file found!")
        return 0

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Load points
        if "points" in data:
            # Convert string colors back to proper format if needed
            for i in range(len(data["points"])):
                if data["points"][i]:
                    # Ensure all elements are strings
                    data["points"][i] = [str(checker) for checker in data["points"][i]]
            game.points = data["points"]

        # Load other data
        if "turn" in data:
            game.turn = str(data["turn"])

        if "dice" in data:
            # Ensure dice is a list of integers
            if isinstance(data["dice"], list):
                game.dice = [int(d) for d in data["dice"]]
            else:
                game.dice = []

        if "bar" in data:
            # Ensure bar has both colors
            game.bar = {"White": 0, "Black": 0}
            if isinstance(data["bar"], dict):
                for color in ["White", "Black"]:
                    if color in data["bar"]:
                        game.bar[color] = int(data["bar"][color])

        if "off" in data:
            # Ensure off has both colors
            game.off = {"White": 0, "Black": 0}
            if isinstance(data["off"], dict):
                for color in ["White", "Black"]:
                    if color in data["off"]:
                        game.off[color] = int(data["off"][color])

        if "selected" in data:
            # Handle "bar" string or None
            if data["selected"] == "bar":
                game.selected = "bar"
            elif data["selected"] is not None:
                game.selected = int(data["selected"])
            else:
                game.selected = None

        moves_count = data.get("moves_count", 0)
        print(f"Game loaded! Turn: {game.turn}, Dice: {game.dice}")
        return moves_count

    except Exception as e:
        print(f"Error loading game: {e}")
        return 0


def save_highscore(winner, loser, moves, winner_score, loser_score):
    try:
        if os.path.exists(HIGHSCORES_FILE):
            with open(HIGHSCORES_FILE, "r") as f:
                scores = json.load(f)
        else:
            scores = []

        scores.append({
            "winner": winner,
            "loser": loser,
            "moves": moves,
            "winner_score": winner_score,
            "loser_score": loser_score
        })

        # Sort by moves (fewer moves = better)
        scores.sort(key=lambda x: x["moves"])

        # Keep only top 20
        scores = scores[:20]

        with open(HIGHSCORES_FILE, "w") as f:
            json.dump(scores, f, indent=2)

    except Exception as e:
        print(f"Error saving high score: {e}")