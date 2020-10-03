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
# bot.add_cog(SortRiddleCog(bot))
bot.load_extension('cog.sort_riddle')


@bot.event
async def on_ready():
    # Bot起動時にターミナルに通知を出す
    print('-'*20)
    print('ログインしました')
    print('-'*20)

# @bot.event
# async def on_guild_join(guild):
#     to_insert_index = bisect.bisect(guild_id_list, guild.id)
#     info = {
#         "guild_id": guild.id,
#         "guild_name": guild.name,
#         "channel_id": None,
#         "answer": None,
#         "question": None,
#         "start_time": None
#     }
#     sort_riddle_data.insert(to_insert_index, info)

#     with open('./info.json', 'w') as f:
#         json.dump(sort_riddle_data, f, indent=4)

#     print('-'*20)
#     print('データを挿入しました')
#     for item in sort_riddle_data:
#         print(item)
#     print('-'*20)


if __name__ == "__main__":
    bot.run(TOKEN)
