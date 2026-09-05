import pandas as pd
from pybaseball import playerid_lookup, statcast_batter


PIRATES_HITTERS = [
    ("Horwitz", "Spencer"),
    ("Lowe", "Brandon"),
    ("Reynolds", "Bryan"),
    ("Valdez", "Esmerlyn"),
    ("Cruz", "Oneil"),
    ("Gonzales", "Nick"),
    ("Gonzalez", "Jacob"),
    ("Triolo", "Jared"),
    ("Davis", "Henry")
]

def create_team_df(player_names, start_date, end_date):
    team_df = pd.DataFrame()

    for player_name in player_names:
        last_name, first_name = player_name
        player = playerid_lookup(last_name, first_name)
        if player.empty:
            print(f"No player found for name: {first_name} {last_name}")
            continue

        player_id = player.iloc[0]["key_mlbam"]

        player_df = statcast_batter(
            start_date,
            end_date,
            player_id
        )

        team_df = pd.concat([team_df, player_df], ignore_index=True)

    return team_df