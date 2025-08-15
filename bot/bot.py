import discord
from discord.ext import commands
from .timer import ping_riot_api_task

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

from . import commands  # Ensure commands are imported after bot is created
import asyncio
from Image_library.images import refresh_patch

async def patch_refresher():
    while True:
        await refresh_patch()
        await asyncio.sleep(60)  # refresh every 1 minute

@bot.event
async def on_ready():
    asyncio.create_task(patch_refresher())
    ping_riot_api_task.start()
      # Start patch refresher
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name='League Of Legends')
    )
    print(f'[Startup] Logged in as {bot.user} and synced commands.')