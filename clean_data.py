import pandas as pd

# the total games played by a MLB to calculate a qualified hitter
total_games_played = 82

def filter_quality_hitters(df):

    # Removes non-qualified hitters
    filtered_df = df[df["PA"] >= total_games_played * 3.1]

    # Keeps necessary columns
    columns_to_keep = ["Player", "Age", "Team", "Lg", "WAR", "G", "PA", "AB", "R", "H", "HR", "RBI", "SB", "BB", "SO", "OBP", "SLG", "OPS", 
    "OPS+", "TB", "SH", "SF", "Pos"]
    filtered_df = df[columns_to_keep]

    # Rename columns for clarity
    filtered_df = filtered_df.rename(columns={
        "Player" : "player",
        "Age" : "age",
        "Team" : "team",
        "Lg" : "league",
        "WAR" : "war",
        "G" : "games",
        "PA" : "plate_appearances",
        "AB" : "at_bats",
        "R" : "runs",
        "H" : "hits",
        "HR" : "homeruns",
        "RBI" : "runs_batted_in",
        "SB" : "stolen_bases",
        "BB" : "bases_on_balls",
        "SO" : "strikeouts",
        "OBP" : "on_base_percentage",
        "SLG" : "slugging_percentage",
        "OPS" : "on_base_plus_slugging_percentage", 
        "OPS+" : "adjusted_on_base_plus_slugging_percentage",
        "TB" : "total_bases",
        "SH" : "sacrifice_hits",
        "SF" : "sacrifice_flys",
        "Pos" : "position"
    })

    # Create useful stat columns
    filtered_df
    return filtered_df