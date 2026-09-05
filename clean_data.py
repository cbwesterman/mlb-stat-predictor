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


    daily_df = (
        team_df.groupby(["game_date", "game_pk", "player_name", "batter"])
        .agg(
            plate_appearances=("events", "count"),
            hits=("events", lambda x: x.isin(["single", "double", "triple", "home_run"]).sum()),
            starting_pitcher_id=("pitcher", "first"),
            starting_pitcher_hand=("p_throws", "first"),
            starting_pitcher_rest_days=("pitcher_days_since_prev_game", "first"),
            batter_rest_days=("batter_days_since_prev_game", "first")
        )
        .reset_index()
    )
    return daily_df