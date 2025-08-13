from discord.ext import tasks

@tasks.loop(seconds=5)
async def ping_riot_api():
    print("Pinging Riot API...")