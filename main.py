# python libraries
import pandas as pd
from pathlib import Path

# .py files
from clean_data import filter_quality_hitters
from model_params import create_model_params
from model import create_model

def main():
    players_df = pd.read_csv("data/mlb_player_stats.csv")
    create_model(*create_model_params(players_df))

if __name__ == "__main__":
    main()