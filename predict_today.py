import requests
from datetime import date

def get_todays_game():
    today = date.today().isoformat()
    response = requests.get(
        "https://statsapi.mlb.com/api/v1/schedule",
        params={"sportId": 1, "date": today, "teamId": 134, "hydrate": "probablePitcher"}
    )
    response.raise_for_status()
    data = response.json()

    if not data["dates"]:
        print("No Pirates game scheduled today.")
        return

    game = data["dates"][0]["games"][0]
    return game

def get_opponent_info(game):
    if game["teams"]["home"]["team"]["id"] == 134:
        pirates_side = "home"
        opponent_side = "away"
    else:
        pirates_side = "away"
        opponent_side = "home"

    opponent_pitcher = game["teams"][opponent_side]["probablePitcher"]
    return opponent_pitcher

def get_pitcher_handedness(pitcher_id):
    response = requests.get(f"https://statsapi.mlb.com/api/v1/people/{pitcher_id}")
    response.raise_for_status()
    data = response.json()
    return data["people"][0]["pitchHand"]["code"]

def get_current_rolling_stats(batter_id, df, n):
    # Use cleaned_output and create rolling stats without shifting.

if __name__ == "__main__":
    print("Running predict_today.py")
    game = get_todays_game()
    if game:
        opponent_pitcher = get_opponent_info(game)
        print(opponent_pitcher)

        hand = get_pitcher_handedness(opponent_pitcher["id"])
        print(hand)