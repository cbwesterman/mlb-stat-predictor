# python libraries
import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

# .py files
from get_team_data import PIRATES_HITTERS, create_team_df
from clean_data import clean_data
from add_pitcher_data import add_pitcher_data

def main():
    START_DATE = "2026-03-25"
    END_DATE = "2026-08-19"
    team_df = create_team_df(PIRATES_HITTERS, START_DATE, END_DATE)
    team_df.to_csv("data/api_output.csv", index=False)

    team_df = clean_data(team_df)
    team_df.to_csv("data/cleaned_output.csv", index=False)

    team_df = add_pitcher_data(team_df, START_DATE, END_DATE)
    team_df.to_csv("data/pitcher_stats_output.csv", index=False)

if __name__ == "__main__":
    main()