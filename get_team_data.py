import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter

# Player Lookups:
batter1 = playerid_lookup("mangum", "jake")
batter2 = playerid_lookup("lowe", "brandon")
batter3 = playerid_lookup("reynolds", "bryan")
batter4 = playerid_lookup("horwitz", "spencer")
batter5 = playerid_lookup("gonzales", "nick")
batter6 = playerid_lookup("simon", "ronny")
batter7 = playerid_lookup("valdez", "esmerlyn")
batter8 = playerid_lookup("gonzalez", "jacob")
batter9 = playerid_lookup("davis", "henry")

batter1_id = batter1.iloc[0]["key_mlbam"]
batter2_id = batter2.iloc[0]["key_mlbam"]
batter3_id = batter3.iloc[0]["key_mlbam"]
batter4_id = batter4.iloc[0]["key_mlbam"]
batter5_id = batter5.iloc[0]["key_mlbam"]
batter6_id = batter6.iloc[0]["key_mlbam"]
batter7_id = batter7.iloc[0]["key_mlbam"]
batter8_id = batter8.iloc[0]["key_mlbam"]
batter9_id = batter9.iloc[0]["key_mlbam"]

PIRATES_HITTER_IDS = [
        batter1_id,
        batter2_id,
        batter3_id,
        batter4_id,
        batter5_id,
        batter6_id,
        batter7_id,
        batter8_id,
        batter9_id
]

def get_team_data(start_date, end_date, player_ids):
    player_dfs = []

    for player_id in player_ids:
        print(f"Gathering data for player ID: {player_id}")

        data = statcast_batter(
                start_date,
                end_date,
                player_id=player_id
        )

        if not data.empty:
            player_dfs.append(data)

    if not player_dfs:
        return pd.DataFrame()

    team_df = pd.concat(player_dfs, ignore_index=True)
    return team_df