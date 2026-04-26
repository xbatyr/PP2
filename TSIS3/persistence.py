import json
import os


BASE_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal",
}


def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
        return default.copy() if isinstance(default, dict) else list(default)

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        save_json(path, default)
        return default.copy() if isinstance(default, dict) else list(default)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_settings():
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS)


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def add_score(name, score, distance, coins):
    scores = load_leaderboard()
    scores.append(
        {
            "name": name or "Player",
            "score": int(score),
            "distance": int(distance),
            "coins": int(coins),
        }
    )
    scores.sort(key=lambda item: (item["score"], item["distance"]), reverse=True)
    scores = scores[:10]
    save_json(LEADERBOARD_FILE, scores)
    return scores
