def prep_for_model(df):
    team_df = df.copy()
    team_df["starting_pitcher_hand_L"] = (team_df["starting_pitcher_hand"] == "L").astype(int)
    return team_df