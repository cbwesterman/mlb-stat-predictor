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

    team_df["hits_vs_L_last_7"] = (
        team_df.groupby("batter")["hits_vs_L"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )
    team_df["hits_vs_R_last_7"] = (
            team_df.groupby("batter")["hits_vs_R"]
            .transform(lambda x: x.shift(1).rolling(7).sum())
    )
    team_df["pas_vs_L_last_7"] = (
            team_df.groupby("batter")["pas_vs_L"]
            .transform(lambda x: x.shift(1).rolling(7).sum())
    )
    team_df["pas_vs_R_last_7"] = (
            team_df.groupby("batter")["pas_vs_R"]
            .transform(lambda x: x.shift(1).rolling(7).sum())
    )
    team_df["hit_rate_vs_L_last_7"] = (
        team_df["hits_vs_L_last_7"] / team_df["pas_vs_L_last_7"]
    ).where(team_df["pas_vs_L_last_7"] > 0)
    team_df["hit_rate_vs_R_last_7"] = (
        team_df["hits_vs_R_last_7"] / team_df["pas_vs_R_last_7"]
    ).where(team_df["pas_vs_R_last_7"] > 0)

    # Due to the fact L pitchers are less prevalant, this is a fallback for when there is a lack of data.
    team_df["hit_rate_vs_L_last_7"] = team_df["hit_rate_vs_L_last_7"].fillna(team_df["hit_rate_last_7"])
    team_df["hit_rate_vs_R_last_7"] = team_df["hit_rate_vs_R_last_7"].fillna(team_df["hit_rate_last_7"])

    return team_df
