import pandas as pd
from pybaseball import playerid_lookup, statcast_batter


PIRATES_HITTERS = [
    ("Cruz", "Oneil"),
    ("Griffin", "Konnor"),
    ("Lowe", "Brandon"),
    ("O'Hearn", "Ryan"),
    ("Gonzales", "Nick"),
    ("Simon", "Ronny"),
    ("Horwitz", "Spencer"),
    ("Mangum", "Jake"),
    ("Davis", "Henry")
]

def create_team_df(player_names, start_date, end_date):
    team_df = pd.DataFrame()
    rows = []

    for player_name in player_names:
        last_name, first_name = player_name
        player = playerid_lookup(last_name, first_name)
        if player.empty:
            print(f"No player found for name: {first_name} {last_name}")
            continue

        player_id = player.iloc[0]["key_mlbam"]

        rows.append({
            "batter_id": player_id,
            "player_name": f"{first_name} {last_name}"
        })

        player_df = statcast_batter(
            start_date,
            end_date,
            player_id
        )

        team_df = pd.concat([team_df, player_df], ignore_index=True)

    player_id_df = pd.DataFrame(rows)
    player_id_df.to_csv("data/lineup_ids.csv", index=False)
    return team_df