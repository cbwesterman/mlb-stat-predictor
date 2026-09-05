# python libraries
import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

# .py files
from get_team_data import PIRATES_HITTERS, create_team_df
from clean_data import clean_data
from add_pitcher_stats import add_pitcher_stats
from add_hitter_stats import add_hitter_stats
from prep_for_model import prep_for_model
from model import build_model

def main():
    START_DATE = "2026-03-25"
    END_DATE = "2026-09-04"
    team_df = create_team_df(PIRATES_HITTERS, START_DATE, END_DATE)
    team_df.to_csv("data/api_output.csv", index=False)

    team_df = clean_data(team_df)
    team_df.to_csv("data/cleaned_output.csv", index=False)

    team_df = add_pitcher_stats(team_df, START_DATE, END_DATE)
    team_df.to_csv("data/pitcher_stats_output.csv", index=False)

    team_df = add_hitter_stats(team_df)
    team_df.to_csv("data/hitter_stats_output.csv", index=False)

    team_df = prep_for_model(team_df)
    team_df.to_csv("data/model_prepped_output.csv", index=False)

    poisson_model, rf_model, results_df = build_model(team_df)
    results_df.to_csv("data/model_output.csv", index=False)

if __name__ == "__main__":
    main()