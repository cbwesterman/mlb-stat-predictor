import pandas as pd
from pybaseball import statcast_pitcher

def add_pitcher_stats(df, start_date, end_date):
    team_df = df
    pitcher_ids = team_df["starting_pitcher_id"].dropna().unique()
    pitcher_stats = []

    for pitcher_id in pitcher_ids:
        pitcher_data = statcast_pitcher(
            start_date,
            end_date,
            pitcher_id
        )
        pitcher_data = pitcher_data[pitcher_data["events"].notna()]

        if pitcher_data.empty:
            continue

        stats = (
            pitcher_data.groupby(["game_date", "game_pk"])
            .agg(
                batters_faced=("events", "count"),
                hits_allowed=("events", lambda x: x.isin(
                    ["single", "double", "triple", "home_run"]).sum()),
                strikeouts=("events", lambda x: (x == "strikeout").sum())
            )
            .reset_index()
        )

        stats["pitcher"] = pitcher_id
        pitcher_stats.append(stats)

    pitcher_games_df = pd.concat(pitcher_stats, ignore_index=True)
    pitcher_games_df = pitcher_games_df.sort_values(["pitcher", "game_date", "game_pk"])

    pitcher_games_df["hits_allowed_last_5"] = (
        pitcher_games_df.groupby("pitcher")["hits_allowed"]
        .transform(lambda x: x.shift(1).rolling(5).sum())
    )
    pitcher_games_df["batters_faced_last_5"] = (
        pitcher_games_df.groupby("pitcher")["batters_faced"]
        .transform(lambda x: x.shift(1).rolling(5).sum())
    )
    pitcher_games_df["strikeouts_last_5"] = (
        pitcher_games_df.groupby("pitcher")["strikeouts"]
        .transform(lambda x: x.shift(1).rolling(5).sum())
    )

    pitcher_games_df["opp_hit_rate_last_5"] = (
        pitcher_games_df["hits_allowed_last_5"] / pitcher_games_df["batters_faced_last_5"]
    )
    pitcher_games_df["opp_k_rate_last_5"] = (
        pitcher_games_df["strikeouts_last_5"] / pitcher_games_df["batters_faced_last_5"]
    )

    team_df = team_df.merge(
        pitcher_games_df[["pitcher", "game_pk", "opp_hit_rate_last_5", "opp_k_rate_last_5"]],
        left_on=["starting_pitcher_id", "game_pk"],
        right_on=["pitcher", "game_pk"],
        how="left"
    )

    team_df = team_df.drop(columns=["pitcher"])

    return team_df