import pandas as pd
import numpy as np

from clean_data import filter_quality_hitters

def create_model_params(df):
    players_df = filter_quality_hitters(df)

    target = "on_base_plus_slugging_percentage"
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

    X = players_df[features]
    y = players_df[target]
    players_df.to_csv("data/model.csv", index=False)

    return X, y