import pandas as pd

def clean_data(df):
    team_df = df
    team_df = team_df[team_df["events"].notna()]

    return team_df