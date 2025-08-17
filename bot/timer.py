from discord.ext import tasks
from api_handler import ping_riot_api
@tasks.loop(minutes=3)
async def ping_riot_api_task():
    from bot.bot import bot
    await ping_riot_api(bot)
