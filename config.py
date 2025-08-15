from dotenv import load_dotenv 
import os
load_dotenv()

DISCORD_API_KEY=os.getenv("DISCORD_API_KEY")
RIOT_API_KEY=os.getenv("RIOT_API_KEY")
DISCORD_CHANNEL_ID=int(os.getenv("DISCORD_CHANNEL_ID"))  # Replace with your channel's ID