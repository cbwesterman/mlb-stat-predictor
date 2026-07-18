import pandas as pd

# the total games played by a MLB to calculate a qualified hitter
total_games_played = 82

def filter_quality_hitters(present_df, future_df):

    # Removes non-qualified hitters
    present_df = present_df[present_df["PA"] >= total_games_played * 3.1]
    future_df = future_df[future_df["PA"] >= total_games_played * 3.1]

    # Keeps necessary columns
    present_cols = ["Player", "Age", "Team", "Lg", "WAR", "G", "PA", "AB", "R", "H", "HR", "RBI", "SB", "BB", "SO", "OBP", "SLG", "OPS", 
    "OPS+", "TB", "SH", "SF", "Pos"]
    present_df = present_df[present_cols]

    future_cols = ["Player", "OPS"]
    future_df = future_df[future_cols]

    # Rename columns for clarity
    present_df = present_df.rename(columns={
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
        "OPS" : "ops_present", 
        "OPS+" : "adjusted_on_base_plus_slugging_percentage",
        "TB" : "total_bases",
        "SH" : "sacrifice_hits",
        "SF" : "sacrifice_flys",
        "Pos" : "position"
    })

    future_df = future_df.rename(columns={
        "Player" : "player",
        "OPS" : "ops_future"
    })

    return present_df, future_df