import pandas as pd


def build_features(pa_df, daily_df):
    pa_df = pa_df.copy()
    daily_df = daily_df.copy()

    daily_df["game_date"] = pd.to_datetime(daily_df["game_date"])

    daily_df = daily_df.sort_values([
        "batter",
        "game_date",
        "game_pk"
    ])

    daily_df["hits_last_7_games"] = (
        daily_df.groupby("batter")["hits"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    daily_df["pa_last_7_games"] = (
        daily_df.groupby("batter")["plate_appearances"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    daily_df["strikeouts_last_7_games"] = (
        daily_df.groupby("batter")["strikeouts"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    daily_df["walks_last_7_games"] = (
        daily_df.groupby("batter")["walks"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    daily_df["total_bases_last_7_games"] = (
        daily_df.groupby("batter")["total_bases"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    daily_df["hit_rate_last_7_games"] = (
        daily_df["hits_last_7_games"] / daily_df["pa_last_7_games"]
    )

    daily_df["strikeout_rate_last_7_games"] = (
        daily_df["strikeouts_last_7_games"] / daily_df["pa_last_7_games"]
    )

    daily_df["walk_rate_last_7_games"] = (
        daily_df["walks_last_7_games"] / daily_df["pa_last_7_games"]
    )

    daily_df["total_bases_per_game_last_7"] = (
        daily_df["total_bases_last_7_games"] / 7
    )

    rolling_columns = [
        "game_date",
        "game_pk",
        "batter",
        "hits_last_7_games",
        "pa_last_7_games",
        "strikeouts_last_7_games",
        "walks_last_7_games",
        "total_bases_last_7_games",
        "hit_rate_last_7_games",
        "strikeout_rate_last_7_games",
        "walk_rate_last_7_games",
        "total_bases_per_game_last_7",
        "target_hit_game"
    ]

    pa_features_df = pa_df.merge(
        daily_df[rolling_columns],
        on=["game_date", "game_pk", "batter"],
        how="left"
    )

    pa_features_df = pa_features_df.dropna()

    return pa_features_df