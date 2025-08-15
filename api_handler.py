from config import RIOT_API_KEY
from players.player import load_players, save_players
import aiohttp
from scoreboard.player_detail import player_detail
RIOT_REGION = "na1"  
MATCH_REGION = "americas"
new_games = []
headers = {"X-Riot-Token": RIOT_API_KEY}

async def ping_riot_api():
    players = load_players("players/players.txt")
    async with aiohttp.ClientSession() as session:
        for player in players.values():
            puuid = player.puuid
            print(f"Checking last match for player: {player.riot_id}")
            last_match = await get_last_match(session, puuid)
            if last_match and last_match != player.last_game_id:
                print(f"Found new match for player: {player.riot_id}")
                new_games.append((last_match))
                player.add_last_game_id(last_match)
            elif last_match == player.last_game_id:
                print(f"Player: {player.riot_id} | No new matches found.")
            else:
                print(f"Could not find last match for player {player.riot_id}")
        await get_match_details(session, new_games)
    save_players("players/players.txt", players)

async def get_puuid(session, riot_id):
    try:
        name, tagline = riot_id.split("#")
    except ValueError:
        print(f"[ERROR] Invalid Riot ID format: {riot_id}")
        return None
    
    url = f"https://{MATCH_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagline}"
    
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            print(f"[ERROR] Failed to get PUUID for {riot_id} | Status: {resp.status}")
            print(await resp.text())
            return None
        data = await resp.json()
        return data.get("puuid")
              
async def get_last_match(session, puuid):
    url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1"
    async with session.get(url, headers=headers) as resp:
        matches = await resp.json()
        return matches[0] if matches else None
    
async def get_match_details(session, match_id):
    for match_id in new_games:
        url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"[ERROR] Failed to get match details for {match_id} | Status: {resp.status}")
                print(await resp.text())
            print_new_game(match_id, await resp.json())
    clear_game_list()

def clear_game_list():
    new_games.clear()

def print_new_game(match_id, game_data):
    info = game_data.get('info', {})
    mode = info.get('gameMode', 'Unknown')
    duration = info.get('gameDuration', 'Unknown')
    participants = info.get('participants', [])

    print(f"  Game ID: {match_id}")
    print(f"  Mode: {mode}")
    print(f"  Duration: {duration} seconds")
    print(f"  Players:")
    for player in participants:
        player1 = player_detail(
            champion_id=player.get('championId'),
            position=player.get('individualPosition'),
            items=[
                player.get(f'item{i}') for i in range(7)
            ],
            team=player.get('teamId'),
            summoner_name=player.get('riotIdGameName') or player.get('summonerName'),
            cs=player.get('totalMinionsKilled', 0) + player.get('neutralMinionsKilled', 0),
            kills=player.get('kills', 0),
            deaths=player.get('deaths', 0),
            assists=player.get('assists', 0),
            gold=player.get('goldEarned', 0)
        )
        player1.print()
        # Try riotIdGameName + riotIdTagline, then summonerName, then fallback
        # name = player.get('riotIdGameName') or player.get('summonerName') or 'Unknown'
        # tagline = player.get('riotIdTagline')
        # team = player.get('teamId', 'Unknown')
        # if name and tagline:
        #     display_name = f"{name}#{tagline}"
        # else:
        #     display_name = name
        # print(f"    - {display_name} (Team {team})")
