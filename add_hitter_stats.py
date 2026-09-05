import pandas as pd

def add_hitter_stats(df):
    team_df = df.sort_values(["batter", "game_date", "game_pk"]).copy()

    team_df["hits_last_7"] = (
        team_df.groupby("batter")["hits"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )
    team_df["pa_last_7"] = (
        team_df.groupby("batter")["plate_appearances"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )
    team_df["hit_rate_last_7"] = team_df["hits_last_7"] / team_df["pa_last_7"]

    

    return team_df
