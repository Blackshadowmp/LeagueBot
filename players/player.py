from dataclasses import dataclass
import aiohttp
from config import RIOT_API_KEY, MATCH_REGION

player_path = "players/players.txt"

@dataclass
class Player:
    riot_id: str
    puuid: str
    last_game_id: str = ""  
    def add_last_game_id(self, game_id: str):
        self.last_game_id = game_id

def load_players():
    players = {}
    with open(player_path, "r") as f:
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

def save_players(players: dict[str, Player]):
    print(f"Saving {len(players)} players to {player_path}")
    with open(player_path, "w") as f:
        for player in players.values():
            f.write(f"{player.riot_id} {player.puuid} {player.last_game_id}\n")

async def add_player(riot_id: str):
    players = load_players()
    player = riot_id.lower()
    if player in players:
        return False

    puuid = await fetch_puuid(riot_id)
    if not puuid:
        print(f"[ERROR] Could not fetch puuid for {riot_id}")
        return False

    players[player] = Player(riot_id=riot_id, puuid=puuid)
    save_players(players)
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
