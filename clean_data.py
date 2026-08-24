import pandas as pd

def clean_data(df):
    team_df = df
    team_df = team_df[team_df["events"].notna()]

    columns_to_keep = [
        "pitch_type",
        "game_date",
        "release_speed",
        "player_name",
        "batter",
        "pitcher",
        "events",
        "spin_dir",
        "game_type",
        "p_throws",
        "home_team",
        "away_team",
        "hit_distance_sc",
        "launch_speed",
        "launch_angle",
        "effective_speed",
        "release_spin_rate",
        "game_pk",
        "estimated_ba_using_speedangle",
        "estimated_woba_using_speedangle",
        "woba_value",
        "woba_denom",
        "delta_home_win_exp",
        "delta_run_exp",
        "estimated_slg_using_speedangle",
        "delta_pitcher_run_exp",
        "home_win_exp",
        "bat_win_exp",
        "pitcher_days_since_prev_game",
        "batter_days_since_prev_game"
    ]

    team_df = team_df[columns_to_keep]

    team_df = pd.get_dummies(
        team_df,
        columns=["pitch_type"],
        prefix="pitch",
        dtype=int
    )

    team_df = pd.get_dummies(
        team_df,
        columns=["p_throws"],
        prefix="p_throws",
        dtype=int
    )
    return team_df