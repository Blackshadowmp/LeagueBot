from bot.bot import bot
from config import DISCORD_API_KEY
from bot.timer import ping_riot_api
if __name__ == '__main__':
    try:
        print('Starting bot...')
        bot.run(DISCORD_API_KEY)
        ping_riot_api.start()
    except Exception as e:
        print(f'Error occurred: {e}')