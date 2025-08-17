import discord
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
from Image_library.images import get_champion_icon, get_item_icon, get_summoner_spell_icon
from players.player import load_players

FONT_PATH = "arial.ttf"

# Image sizes
CHAMP_SIZE = 48
ITEM_SIZE = 32
ROW_HEIGHT = 64
WIDTH = 800

async def fetch_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            return Image.open(io.BytesIO(data)).convert("RGBA")

async def create_team_image(team_players):
    height = ROW_HEIGHT * len(team_players)
    canvas = Image.new("RGBA", (WIDTH, height), (30, 30, 30, 255))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_PATH, 18)

    y_offset = 0

    for player in team_players:
        # Champion icon
        champ_icon = await fetch_image(get_champion_icon(player.champion_id))
        champ_icon = champ_icon.resize((CHAMP_SIZE, CHAMP_SIZE))
        canvas.paste(champ_icon, (10, y_offset), champ_icon)

        # Player stats text
        stats_text = f"{player.summoner_name} | {player.kills}/{player.deaths}/{player.assists} | CS: {player.cs} | Gold: {player.gold}"
        draw.text((70, y_offset + 12), stats_text, font=font, fill=(255, 255, 255))

        # Item icons
        item_x = 475
        for item in player.items:
            if item and int(item) > 0:
                item_icon = await fetch_image(get_item_icon(item))
                item_icon = item_icon.resize((ITEM_SIZE, ITEM_SIZE))
                canvas.paste(item_icon, (item_x, y_offset + 16), item_icon)
                item_x += ITEM_SIZE + 4
                # Summoner spell icons
       
        spell1_icon = await fetch_image(get_summoner_spell_icon(player.summoner_spell1))
        spell2_icon = await fetch_image(get_summoner_spell_icon(player.summoner_spell2))
        spell1_icon = spell1_icon.resize((ITEM_SIZE, ITEM_SIZE))
        spell2_icon = spell2_icon.resize((ITEM_SIZE, ITEM_SIZE))

        canvas.paste(spell1_icon, (item_x, y_offset + 16), spell1_icon)
        canvas.paste(spell2_icon, (item_x + ITEM_SIZE + 4, y_offset + 16), spell2_icon)
        y_offset += ROW_HEIGHT

    # Save to BytesIO
    img_bytes = io.BytesIO()
    canvas.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes

async def send_game_to_discord(channel, blue_team, red_team, match_id, winning_team):
    # Generate images
    blue_image = await create_team_image(blue_team)
    red_image = await create_team_image(red_team)

    blue_file = discord.File(blue_image, filename="blue_team.png")
    red_file = discord.File(red_image, filename="red_team.png")
    # Embeds
    match= match_id.split("_")[-1]
    blue_embed = discord.Embed(title="Blue Team Wins" if winning_team == 100 else "Blue Team Lost", color=0x0000FF, url=f"https://www.leagueofgraphs.com/match/na/{match}")
    blue_embed.set_image(url="attachment://blue_team.png")

    red_embed = discord.Embed(title="Red Team Wins" if winning_team == 200 else "Red Team Lost", color=0x992d22)
    red_embed.set_image(url="attachment://red_team.png")
    tracked_players = [player.split('#')[0] for player in load_players("players/players.txt")]
    players_to_print=[]
    for player in blue_team + red_team: 
        if player.summoner_name.lower() in tracked_players:
            players_to_print.append(str(player.summoner_name))
    # Send both embeds in one message
    #send a message saying who in the tracked list is in the game
    await channel.send("Players in the game: " + ", ".join(players_to_print))
    await channel.send(files=[blue_file, red_file], embeds=[blue_embed, red_embed])
