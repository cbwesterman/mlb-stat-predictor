# python libraries
import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

# .py files
from get_team_data import PIRATES_HITTERS, create_team_df
from clean_data import clean_data

def main():
    team_df = create_team_df(PIRATES_HITTERS)
    team_df.to_csv("data/api_output.csv", index=False)

    team_df = clean_data(team_df)
    team_df.to_csv("data/cleaned_output.csv", index=False)

if __name__ == "__main__":
    main()