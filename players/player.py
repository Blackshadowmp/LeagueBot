from dataclasses import dataclass
import aiohttp
import asyncio
from config import RIOT_API_KEY

player_path = "players/players.txt"
MATCH_REGION = "americas" 

@dataclass
class Player:
    riot_id: str
    puuid: str
    last_game_id: str = ""  
    def add_last_game_id(self, game_id: str):
        self.last_game_id = game_id

def load_players(filename):
    players = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3: # all Data exist already
                riot_id, puuid, last_game_id = parts
            elif len(parts) == 2:#Just added/no games played
                riot_id, puuid = parts
                last_game_id = ""
            else:
                continue
            players[riot_id.lower()] = Player(riot_id=riot_id, puuid=puuid, last_game_id=last_game_id)
    return players

def save_players(filename, players):
    with open(filename, "w") as f:
        for player in players.values():
            f.write(f"{player.riot_id} {player.puuid} {player.last_game_id}\n")

async def add_player(riot_id: str):
    players = load_players(player_path)
    player = riot_id.lower()
    if player in players:
        return False

    puuid = await fetch_puuid(riot_id)
    if not puuid:
        print(f"[ERROR] Could not fetch puuid for {riot_id}")
        return False

    players[player] = Player(riot_id=riot_id, puuid=puuid)
    save_players(player_path, players)
    return True

async def fetch_puuid(riot_id: str):
    try:
        name, tagline = riot_id.split("#")
    except ValueError:
        print(f"[ERROR] Invalid Riot ID format: {riot_id}")
        return None
    
    url = f"https://{MATCH_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
    headers = {"X-Riot-Token": RIOT_API_KEY.strip()}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"[ERROR] Failed to get PUUID for {riot_id} | Status: {resp.status}")
                print(await resp.text())
                return None
            data = await resp.json()
            return data.get("puuid")

# # Example usage:
# # Access or add a new player
# puuid = "Steviesaysrawr#na1"
# add_player(puuid)

# players = load_players(player_path)

# # Update last game ID for a player
# players[puuid].last_game_id = "1234567890"
# save_players(player_path, players)
