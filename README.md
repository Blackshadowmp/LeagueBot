# LeagueBot

LeagueBot is a Discord bot that integrates with the Riot Games API to provide League of Legends data and updates directly in your Discord server.

---

## Features
- Connects to Riot Games API for live match and player data.
- Sends updates and notifications into a specified Discord channel.
- Easy configuration using environment variables.

---

## Prerequisites
- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- Discord Bot Token ([guide](https://discordpy.readthedocs.io/en/stable/discord.html))
- Riot Games API Key ([get one here](https://developer.riotgames.com/))

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Blackshadowmp/LeagueBot.git
   cd LeagueBot
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

You must create a `.env` file in the **root directory** of the project with the following values:

```env
DISCORD_API_KEY=your_discord_bot_token_here
RIOT_API_KEY=your_riot_api_key_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here
```

- `DISCORD_API_KEY` → Your Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
- `RIOT_API_KEY` → Your Riot Games API key from the [Riot Developer Portal](https://developer.riotgames.com/).
- `DISCORD_CHANNEL_ID` → The numeric channel ID where the bot will send updates.

---

## Usage

Run the bot with:

```bash
python app.py
```

If everything is configured correctly, your bot will log in to Discord and start sending League of Legends updates.

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License
This project is licensed under the [MIT License](LICENSE).
