import requests
import pandas as pd
import numpy as np
import joblib
import statsmodels.api as sm
from datetime import date, timedelta
from pybaseball import statcast_pitcher

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

def get_batter_rolling_stats(batter_id, df, n=7):
    batter_rows = df[df["batter"] == batter_id].sort_values(["game_date", "game_pk"])
    recent = batter_rows.tail(n)

    hits_last_7 = recent["hits"].sum()
    pa_last_7 = recent["plate_appearances"].sum()
    hit_rate_last_7 = hits_last_7 / pa_last_7 if pa_last_7 > 0 else None

    hits_vs_L = recent["hits_vs_L"].sum()
    pas_vs_L = recent["pas_vs_L"].sum()
    hit_rate_vs_L = hits_vs_L / pas_vs_L if pas_vs_L > 0 else hit_rate_last_7

    hits_vs_R = recent["hits_vs_R"].sum()
    pas_vs_R = recent["pas_vs_R"].sum()
    hit_rate_vs_R = hits_vs_R / pas_vs_R if pas_vs_R > 0 else hit_rate_last_7

    return {
        "hits_last_7": hits_last_7,
        "pa_last_7": pa_last_7,
        "hit_rate_last_7": hit_rate_last_7,
        "hit_rate_vs_L_last_7": hit_rate_vs_L,
        "hit_rate_vs_R_last_7": hit_rate_vs_R,
    }

def get_pitcher_rolling_stats(pitcher_id, n=5):
    end_date = date.today().isoformat()
    start_date = (date.today() - timedelta(days=45)).isoformat()

    pitcher_data = statcast_pitcher(start_date, end_date, pitcher_id)
    pitcher_data = pitcher_data[pitcher_data["events"].notna()]

    if pitcher_data.empty:
        return None

    stats = (
        pitcher_data.groupby(["game_date", "game_pk"])
        .agg(
            batters_faced=("events", "count"),
            hits_allowed=("events", lambda x: x.isin(
                ["single", "double", "triple", "home_run"]).sum()),
            strikeouts=("events", lambda x: (x == "strikeout").sum())
        )
        .reset_index()
        .sort_values(["game_date", "game_pk"])
    )

    recent = stats.tail(n)

    batters_faced = recent["batters_faced"].sum()
    hits_allowed = recent["hits_allowed"].sum()
    strikeouts = recent["strikeouts"].sum()

    opp_hit_rate_last_5 = hits_allowed / batters_faced if batters_faced > 0 else None
    opp_k_rate_last_5 = strikeouts / batters_faced if batters_faced > 0 else None

    return {
        "opp_hit_rate_last_5": opp_hit_rate_last_5,
        "opp_k_rate_last_5": opp_k_rate_last_5,
    }

if __name__ == "__main__":
    print("Running predict_today.py")

    cleaned_output = pd.read_csv("data/cleaned_output.csv", parse_dates=["game_date"])

    tracked_batters = pd.read_csv("data/lineup_ids.csv")
    tracked_batters = tracked_batters.dropna(subset=["batter_id"])
    tracked_batters["batter_id"] = tracked_batters["batter_id"].astype(int)

    tracked_batter_ids = tracked_batters["batter_id"].tolist()
    id_to_name = dict(zip(tracked_batters["batter_id"], tracked_batters["player_name"]))

    game = get_todays_game()
    if not game:
        exit()

    opponent_pitcher = get_opponent_info(game)
    hand = get_pitcher_handedness(opponent_pitcher["id"])
    pitcher_stats = get_pitcher_rolling_stats(opponent_pitcher["id"])

    if pitcher_stats is None:
        print("No recent data for pitcher. Unable to generate predictions.")
        exit()

    poisson_model = joblib.load("poisson_model.pkl")
    rf_model = joblib.load("rf_model.pkl")

    model_features = [
        "hits_last_7",
        "pa_last_7",
        "hit_rate_last_7",
        "opp_hit_rate_last_5",
        "opp_k_rate_last_5",
        "starting_pitcher_hand_L",
        "hit_rate_vs_L_last_7",
        "hit_rate_vs_R_last_7",
    ]

    results = []

    for batter_id in tracked_batter_ids:
        hitter_stats = get_batter_rolling_stats(batter_id, cleaned_output)

        if hitter_stats["pa_last_7"] == 0:
            print(f"Skipping batter {batter_id} — no recent PA data")
            continue

        row = {
            **hitter_stats,
            **pitcher_stats,
            "starting_pitcher_hand_L": 1 if hand == "L" else 0,
        }

        X = pd.DataFrame([row])[model_features]
        exposure = row["pa_last_7"] / 7

        X_c = sm.add_constant(X, has_constant="add")
        poisson_pred = poisson_model.predict(X_c, offset=np.log(exposure))

        X_rf = X.copy()
        X_rf["exposure"] = exposure
        rf_pred = rf_model.predict(X_rf)

        results.append({
            "batter_id": batter_id,
            "player_name": id_to_name.get(batter_id, "Unknown"),
            "poisson_pred": round(poisson_pred.values[0], 2),
            "rf_pred": round(rf_pred[0], 2),
        })

    results_df = pd.DataFrame(results)
    print(results_df)