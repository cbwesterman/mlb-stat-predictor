import pandas as pd


def clean_data(df):
    pa_df = df[df["events"].notna()].copy()

    pa_df["game_date"] = pd.to_datetime(pa_df["game_date"])

    pa_df = pa_df.sort_values([
        "game_date",
        "game_pk",
        "player_name",
        "batter",
        "at_bat_number"
    ])

    pa_df["single"] = (pa_df["events"] == "single").astype(int)
    pa_df["double"] = (pa_df["events"] == "double").astype(int)
    pa_df["triple"] = (pa_df["events"] == "triple").astype(int)
    pa_df["home_run"] = (pa_df["events"] == "home_run").astype(int)

    pa_df["hit"] = pa_df["events"].isin([
        "single",
        "double",
        "triple",
        "home_run"
    ]).astype(int)

    pa_df["walk"] = (pa_df["events"] == "walk").astype(int)
    pa_df["strikeout"] = (pa_df["events"] == "strikeout").astype(int)

    pa_df["total_bases"] = (
        pa_df["single"]
        + 2 * pa_df["double"]
        + 3 * pa_df["triple"]
        + 4 * pa_df["home_run"]
    )

    daily_df = (
        pa_df.groupby(["game_date", "game_pk", "player_name", "batter"])
        .agg(
            plate_appearances=("events", "count"),
            hits=("hit", "sum"),
            singles=("single", "sum"),
            doubles=("double", "sum"),
            triples=("triple", "sum"),
            home_runs=("home_run", "sum"),
            walks=("walk", "sum"),
            strikeouts=("strikeout", "sum"),
            total_bases=("total_bases", "sum")
        )
        .reset_index()
    )

    daily_df["target_hit_game"] = (daily_df["hits"] >= 1).astype(int)

    return pa_df, daily_df