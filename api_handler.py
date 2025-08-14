from config import RIOT_API_KEY
from players.player import load_players, save_players
import aiohttp

RIOT_REGION = "na1"  
MATCH_REGION = "americas"

async def ping_riot_api():
    players = load_players("players/players.txt")
    async with aiohttp.ClientSession() as session:
        for player in players.values():
            puuid = player.puuid
            print(f"Checking last match for player: {player.riot_id}")
            last_match = await get_last_match(session, puuid)
            if last_match and last_match != player.last_game_id:
                print(f"Found new match for player: {player.riot_id}")
                player.add_last_game_id(last_match)
            elif last_match == player.last_game_id:
                print(f"Player: {player.riot_id} | No new matches found.")
            else:
                print(f"Could not find last match for player {player.riot_id}")
    save_players("players/players.txt", players)

async def get_puuid(session, riot_id):
    try:
        name, tagline = riot_id.split("#")
    except ValueError:
        print(f"[ERROR] Invalid Riot ID format: {riot_id}")
        return None
    
    url = f"https://{MATCH_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
    headers = {"X-Riot-Token": RIOT_API_KEY.strip()}
    
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            print(f"[ERROR] Failed to get PUUID for {riot_id} | Status: {resp.status}")
            print(await resp.text())
            return None
        data = await resp.json()
        return data.get("puuid")
              
async def get_last_match(session, puuid):
    url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    async with session.get(url, headers=headers) as resp:
        matches = await resp.json()
        print(matches)
        return matches[0] if matches else None
