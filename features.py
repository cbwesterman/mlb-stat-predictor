import pandas as pd

def build_features(df):

    features_df = df.copy()

    features_df = features_df.sort_values(["player_name", "game_date", "game_pk"])

    features_df["hits_last_7"] = (
        features_df.groupby("player_name")["hits"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    features_df["pa_last_7"] = (
        features_df.groupby("player_name")["plate_appearances"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    features_df["strikeouts_last_7"] = (
        features_df.groupby("player_name")["strikeouts"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    features_df["total_bases_last_7"] = (
        features_df.groupby("player_name")["total_bases"]
        .transform(lambda x: x.shift(1).rolling(7).sum())
    )

    # Last 7 games rates
    features_df["hit_rate_last_7"] = (
        features_df["hits_last_7"] / features_df["pa_last_7"]
    )

    features_df["strikeout_rate_last_7"] = (
        features_df["strikeouts_last_7"] / features_df["pa_last_7"]
    )

    features_df["total_bases_per_game_last_7"] = (
        features_df["total_bases_last_7"] / 7
    )

    features_df = features_df.dropna()

    return features_df