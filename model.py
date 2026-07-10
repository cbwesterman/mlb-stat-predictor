import pandas as pd

from clean_data import filter_quality_hitters
from sklearn.model_selection import train_test_split

def create_model_csv():
    players_df = pd.read_csv("data/mlb_player_stats.csv")
    players_df = filter_quality_hitters(players_df)

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
        "slugging_percentage",
        "total_bases",
        "sacrifice_hits",
        "sacrifice_flys"
    ]

    X = players_df[features]
    y = players_df[target]

    players_df.to_csv("data/ml_ready_player_stats.csv", index=False)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
)