
import discord
from discord.ext import commands
from .timer import ping_riot_api_task

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

from . import commands  # Ensure commands are imported after bot is created

@bot.event
async def on_ready():
    ping_riot_api_task.start()
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name='League Of Legends')
    )
    print(f'[Startup] Logged in as {bot.user} and synced commands.')