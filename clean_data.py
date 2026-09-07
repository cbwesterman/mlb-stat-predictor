import pandas as pd

def clean_data(df):
    team_df = df
    team_df = team_df[team_df["events"].notna()]

    columns_to_keep = [
        "game_date",
        "game_pk",
        "events",
        "player_name",
        "batter",
        "game_type",
        "home_team",
        "away_team",
        "pitcher",
        "p_throws",
        "pitcher_days_since_prev_game",
        "batter_days_since_prev_game"
    ]

    team_df = team_df[columns_to_keep]
    team_df = team_df[team_df["game_type"] == "R"]

    hit_events = ["single", "double", "triple", "home_run"]
    team_df["is_hit"] = team_df["events"].isin(hit_events).astype(int)
    team_df["pa_vs_L"] = (team_df["p_throws"] == "L").astype(int)
    team_df["pa_vs_R"] = (team_df["p_throws"] == "R").astype(int)
    team_df["hits_vs_L"] = team_df["pa_vs_L"] * team_df["is_hit"]
    team_df["hits_vs_R"] = team_df["pa_vs_R"] * team_df["is_hit"]

    daily_df = (
        team_df.groupby(["game_date", "game_pk", "player_name", "batter"])
        .agg(
            plate_appearances=("events", "count"),
            hits=("events", lambda x: x.isin(hit_events).sum()),
            starting_pitcher_id=("pitcher", "first"),
            starting_pitcher_hand=("p_throws", "first"),
            starting_pitcher_rest_days=("pitcher_days_since_prev_game", "first"),
            batter_rest_days=("batter_days_since_prev_game", "first"),
            hits_vs_L=("hits_vs_L", "sum"),
            hits_vs_R=("hits_vs_R", "sum"),
            pas_vs_L=("pa_vs_L", "sum"),
            pas_vs_R=("pa_vs_R", "sum")
        )
        .reset_index()
    )
    return daily_df