import discord
from discord import Option
from players.player import add_player
from bot.bot import bot
@bot.slash_command(name="add", description="Create a new player with the given PUUID ex: DollarBill#Money")
async def create_player(ctx: discord.ApplicationContext, puuid=Option(str, "Enter the Riot ID, e.g. Steviesaysrawr#na1", required=True)):
    if(add_player(puuid)):
        await ctx.respond(f"Player {puuid.lower()} created successfully.")
    else:
        await ctx.respond(f"Player {puuid.lower()} already exists.")