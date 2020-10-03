import bisect
import configparser
import time

import discord
from discord.ext.commands import Bot

from cog.sort_riddle import SortRiddleCog

config = configparser.ConfigParser()
config.read('./config.ini')
TOKEN = config['TOKEN']['token']

bot = Bot(command_prefix='/')
bot.load_extension('cog.sort_riddle')


@bot.event
async def on_ready():
    # Bot起動時にターミナルに通知を出す
    print('-'*20)
    print('ログインしました')
    print('-'*20)

if __name__ == "__main__":
    bot.run(TOKEN)
