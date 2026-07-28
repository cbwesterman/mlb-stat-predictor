import pandas as pd
import numpy as np

from clean_data import filter_quality_hitters

def create_model_params(present_df, future_df):
    present_df, future_df = filter_quality_hitters(present_df, future_df)
    model_df = present_df.merge(
        future_df,
        on="player",
        how="inner"
    )

    target = "ops_future"
    features = [
        "war",
        "plate_appearances",
        "runs",
        "hits",
        "homeruns",
        "runs_batted_in",
        "bases_on_balls",
        "strikeouts",
        "total_bases",
        "sacrifice_hits",
        "sacrifice_flys"
    ]

    X = model_df[features]
    y = model_df[target]
    model_df.to_csv("data/model.csv", index=False)

    return X, y