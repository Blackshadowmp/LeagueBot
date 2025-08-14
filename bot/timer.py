from discord.ext import tasks
from api_handler import ping_riot_api

@tasks.loop(minutes=1)
async def ping_riot_api_task():
    await ping_riot_api()
