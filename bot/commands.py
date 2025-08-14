import discord
from discord import Option
from players.player import add_player
from bot.bot import bot
@bot.slash_command(name="add", description="Create a new player with the given PUUID ex: DollarBill#Money")
async def create_player(ctx: discord.ApplicationContext, riot_id=Option(str, "Enter the Riot ID, e.g. Steviesaysrawr#na1", required=True)):
    if( await add_player(riot_id)):
        await ctx.respond(f"Player {riot_id.lower()} created successfully.")
    else:
        await ctx.respond(f"Issues adding player, already exists, or API issues")