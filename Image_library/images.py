import aiohttp
import asyncio
from .champion_map import champion_id_map
from .summoner_spell_map import summoner_spell_map

fallback_image_url = 'E:/LeagueBot/LeagueBot/Image_library/Missing64x64.jpg'
_patch = None

async def refresh_patch():
    global _patch
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ddragon.leagueoflegends.com/api/versions.json") as resp:
            if resp.status != 200:
                print(f"[ERROR] Failed to get patch list: {resp.status}")
                return
            versions = await resp.json()
            _patch = versions[0]
            print(f"[INFO] Refreshed patch: {_patch}")

def get_patch():
    return _patch or "14.15.1"  # fallback to a recent patch

def get_champion_icon(champion_id: int):
    champion_name = champion_id_map.get(champion_id)
    if not champion_name:
        print(f"[ERROR] Unknown champion ID: {champion_id}")
        return fallback_image_url
    patch = get_patch()
    return f"https://ddragon.leagueoflegends.com/cdn/{patch}/img/champion/{champion_name}.png"

def get_item_icon(item_id: int):
    patch = get_patch()
    return f"https://ddragon.leagueoflegends.com/cdn/{patch}/img/item/{item_id}.png"

def get_summoner_spell_icon(summoner_spell_id: int):
    summoner_spell_name = summoner_spell_map.get(summoner_spell_id)
    patch = get_patch()
    return f"https://ddragon.leagueoflegends.com/cdn/{patch}/img/spell/{summoner_spell_name}.png"