# python libraries
import pandas as pd
from pathlib import Path

# .py files
from clean_data import filter_quality_hitters
from model_params import create_model_params
from model import create_model

def main():
    present_df = pd.read_csv("data/stats_2024.csv")
    future_df = pd.read_csv("data/stats_2025.csv")
    create_model(*create_model_params(present_df, future_df))

if __name__ == "__main__":
    main()