import asyncio
import aiohttp
from images import get_champion_icon, get_item_icon

async def main():
    async with aiohttp.ClientSession() as session:
        item_icon = await get_item_icon(session, 3031)
        champion_icon = await get_champion_icon(session, "Kled")

        print("Item icon result:", item_icon if item_icon else "Item not found")
        print("Champion icon result:", champion_icon if champion_icon else "Champion not found")

if __name__ == "__main__":
    asyncio.run(main())
