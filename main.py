# python libraries
import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

# .py files
from clean_data import clean_data
from features import build_features
from model import build_model

def main():

    ply_lookup = playerid_lookup("reynolds", "bryan")
    ply_id = ply_lookup.iloc[0]["key_mlbam"]
    data = statcast_batter(
        "2026-03-25",
        "2026-07-26",
        player_id=ply_id
    )

    data.to_csv("data/api_output.csv", index=False)
    filtered_data = clean_data(data)
    filtered_data.to_csv("data/filtered_output.csv", index=False)
    features_data = build_features(filtered_data)
    features_data.to_csv("data/features_output.csv", index=False)

    model, results_df = build_model(features_data)
    results_df.to_csv("data/model_output.csv", index=False)

    print(results_df.head())

if __name__ == "__main__":
    main()