import aiohttp
fallback_image_url = 'E:/LeagueBot/LeagueBot/Image_library/Missing64x64.jpg'
async def get_latest_patch(session: aiohttp.ClientSession):
    async with session.get("https://ddragon.leagueoflegends.com/api/versions.json") as resp:
        if resp.status != 200:
            raise RuntimeError(f"Failed to get patch list: {resp.status}")
        versions = await resp.json()
        patch = versions[0]  # latest patch
    return patch

async def get_champion_icon(session: aiohttp.ClientSession, champion_name: str):
    patch = await get_latest_patch(session)
    url = f"https://ddragon.leagueoflegends.com/cdn/{patch}/img/champion/{champion_name}.png"
    async with session.get(url) as resp:
        if resp.status == 200:
            return url
        print(f"Champion icon not found for: {champion_name} (status {resp.status})")
        return fallback_image_url

async def get_item_icon(session: aiohttp.ClientSession, item_id: int):
    patch = await get_latest_patch(session)
    url = f"https://ddragon.leagueoflegends.com/cdn/{patch}/img/item/{item_id}.png"
    async with session.get(url) as resp:
        if resp.status == 200:
            return url
        print(f"Item icon not found for ID: {item_id} (status {resp.status})")
        return fallback_image_url
