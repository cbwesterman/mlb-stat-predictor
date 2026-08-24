import pandas as pd
from pybaseball import statcast_pitcher

def add_pitcher_data(df, start_date, end_date):
    team_df = df
    pitcher_ids = team_df["pitcher"].unique()
    pitcher_stats = []

    for pitcher_id in pitcher_ids:
        pitcher_data = statcast_pitcher(
            start_date,
            end_date,
            pitcher_id
        )

        if pitcher_data.empty:
            continue

        stats = {
            "pitcher": pitcher_id,
            "avg_release_speed": pitcher_data["release_speed"].mean(),
            "avg_spin_rate": pitcher_data["release_spin_rate"].mean(),
            "avg_pfx_x": pitcher_data["pfx_x"].mean(),
            "avg_pfx_z": pitcher_data["pfx_z"].mean()
        }

        pitcher_stats.append(stats)

    pitcher_stats_df = pd.DataFrame(pitcher_stats)

    team_df = team_df.merge(
        pitcher_stats_df,
        on="pitcher",
        how="left"
    )

    return team_df