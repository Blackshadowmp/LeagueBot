import asyncio
from config import RIOT_API_KEY, DISCORD_CHANNEL_ID, MATCH_REGION, GAME_MODES_TO_CHECK
from players.player import load_players, save_players
import aiohttp
from scoreboard.player_detail import player_detail
from scoreboard.team import team
from bot.discord_response import send_game_to_discord


headers = {"X-Riot-Token": RIOT_API_KEY}
new_games = []

async def ping_riot_api(bot):
    players = load_players() 
    async with aiohttp.ClientSession() as session:
        for player in players.values():
            puuid = player.puuid
            print(f"Checking last match for player: {player.riot_id}")
            try:
                last_match = await get_last_match(session, puuid)
            except Exception as e:
                print(f"[ERROR] Failed to get last match for {player.riot_id} | Error: {e}")
                continue
            if last_match and last_match != player.last_game_id:
                print(f"Found new match for player: {player.riot_id}")
                player.add_last_game_id(last_match)
                if last_match not in new_games:
                    new_games.append(last_match)
            elif last_match == player.last_game_id:
                print(f"Player: {player.riot_id} | No new matches found.")
            else:
                print(f"Could not find last match for player {player.riot_id}")
        await get_match_details(session, bot)  
    if new_games:
        save_players(players)
        clear_games(new_games)

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
    
async def get_match_details(session, bot):
    for match_id in new_games:
        url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"[ERROR] Failed to get match details for {match_id} | Status: {resp.status}")
            print_new_game(match_id, await resp.json(), bot)
            await asyncio.sleep(2)

def clear_games(games):
    games.clear()

def print_new_game(match_id, game_data, bot):
    winning_team = None
    info = game_data.get('info', {})
    game_mode = info.get('gameMode')
    if game_mode not in GAME_MODES_TO_CHECK:
        return
    for team_loop in info.get("teams", []):
        if team_loop.get("win") == True:
            winning_team = team_loop.get("teamId")

    participants = info.get('participants', [])
    blue_team = team(100, [])
    red_team = team(200, [])

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
            gold=player.get('goldEarned', 0),
            summoner_spell1=player.get('summoner1Id'),
            summoner_spell2=player.get('summoner2Id')
        )
        if player1.team == 100:
            blue_team.player_list.append(player1)
        else:
            red_team.player_list.append(player1)

    blue_team = blue_team.get_organized_team()
    red_team = red_team.get_organized_team()
    blue_team_players = [p for p in blue_team if p]
    red_team_players = [p for p in red_team if p]

    if DISCORD_CHANNEL_ID is not None:
        channel_obj = bot.get_channel(DISCORD_CHANNEL_ID)
        if channel_obj:
            asyncio.create_task(send_game_to_discord(channel_obj, blue_team_players, red_team_players, match_id, winning_team))
        else:
            print(f"[ERROR] Could not find Discord channel OBJECT with ID {DISCORD_CHANNEL_ID}")
    else:
        print(f"[ERROR] Could not find Discord channel with ID {DISCORD_CHANNEL_ID}")