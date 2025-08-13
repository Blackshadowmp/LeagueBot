from dataclasses import dataclass

player_path = "players/players.txt"

@dataclass
class Player:
    puuid: str
    last_game_id: str = ""  

def load_players(filename):
    players = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                puuid, last_game_id = parts
            elif len(parts) == 1:
                puuid, last_game_id = parts[0], ""
            else:
                continue
            players[puuid] = Player(puuid, last_game_id)
    return players
def add_player(puuid: str):
    players = load_players(player_path)
    key = puuid.lower()  # normalize to lowercase
    if key not in (player.puuid.lower() for player in players.values()):
        players[key] = Player(puuid=key)  
        save_players(player_path, players)
        return True
    return False


def save_players(filename, players):
    with open(filename, "w") as f:
        for player in players.values():
            f.write(f"{player.puuid} {player.last_game_id}\n")

# # Example usage:
# # Access or add a new player
# puuid = "Steviesaysrawr#na1"
# add_player(puuid)

# players = load_players(player_path)

# # Update last game ID for a player
# players[puuid].last_game_id = "1234567890"
# save_players(player_path, players)
