import pandas as pd

def clean_data(df):

    pa_df = df[df["events"].notna()].copy()

    daily_df = (
        pa_df.groupby(["game_date", "game_pk", "player_name", "batter"])
        .agg(
            plate_appearances=("events", "count"),
            hits=("events", lambda x: x.isin(["single", "double", "triple", "home_run"]).sum()),
            singles=("events", lambda x: (x == "single").sum()),
            doubles=("events", lambda x: (x == "double").sum()),
            triples=("events", lambda x: (x == "triple").sum()),
            home_runs=("events", lambda x: (x == "home_run").sum()),
            strikeouts=("events", lambda x: (x == "strikeout").sum())
        )
        .reset_index()
    )

    daily_df["total_bases"] = (
        daily_df["singles"]
        + 2 * daily_df["doubles"]
        + 3 * daily_df["triples"]
        + 4 * daily_df["home_runs"]
    )

    daily_df["target_hit"] = (daily_df["hits"] >= 1).astype(int)

    return daily_df