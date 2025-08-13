from bot.bot import bot
from config import DISCORD_API_KEY
if __name__ == '__main__':
    try:
        print('Starting bot...')
        bot.run(DISCORD_API_KEY)
    except Exception as e:
        print(f'Error occurred: {e}')