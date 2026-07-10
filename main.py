# python libraries
import pandas as pd
from pathlib import Path

# .py files
from clean_data import filter_quality_hitters

def main():
    players_df = pd.read_csv("data/mlb_player_stats.csv")
    players_df = filter_quality_hitters(players_df)
    players_df.to_csv("data/cleaned_mlb_player_stats.csv", index=False)

if __name__ == "__main__":
    main()