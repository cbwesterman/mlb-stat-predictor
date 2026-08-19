# python libraries
import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

# .py files
from clean_data import clean_data
from features import build_features
from model import build_model
from get_team_data import get_team_data, PIRATES_HITTER_IDS

def main():

    data = get_team_data(
        "2026-03-25",
        "2026-08-08",
        PIRATES_HITTER_IDS
    )

    data.to_csv("data/api_output.csv", index=False)
    pa_df, daily_df = clean_data(data)
    pa_df.to_csv("data/pa_output.csv", index=False)
    daily_df.to_csv("data/daily_output.csv", index=False)
    features_data = build_features(pa_df, daily_df)
    features_data.to_csv("data/features_output.csv", index=False)

    model, results_df = build_model(features_data)
    results_df.to_csv("data/model_output.csv", index=False)

    print(results_df.head())

if __name__ == "__main__":
    main()