import bisect
# import configparser
import json

import discord
import pandas as pd
from discord.ext import commands
from discord.ext.commands.core import command


class SortRiddleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sort_riddle_data = []
        self.guild_id_list = []
        try:
            self.guild_id_list = pd.read_csv(
                './data/guild_id_list.csv', header=None)
        except pd.errors.EmptyDataError as e:
            print(f"{'./data/guild_id_list.csv'}が空です\n{e}")
        try:
            with open('./data/sort_riddle_data.json') as f:
                self.sort_riddle_data = json.load(f)
        except:
            print('なんかのエラー')

    @commands.command()
    async def neko(self,ctx):
        await ctx.send(f'{ctx.author.mention} にゃーん')

    @commands.command()
    async def show(self, ctx):
        for item in self.sort_riddle_data:
            await ctx.send(item)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        to_insert_index = bisect.bisect(self.guild_id_list, guild.id)
        info = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "channel_id": None,
            "answer": None,
            "question": None,
            "start_time": None
        }
        self.sort_riddle_data.insert(to_insert_index, info)

        with open('./data/sort_riddle_data.json', 'w') as f:
            json.dump(self.sort_riddle_data, f, indent=4)

        # print('-'*20)
        # print('データを挿入しました')
        # for item in self.sort_riddle_data:
        #     print(item)
        # print('-'*20)

        bisect.insort(self.guild_id_list, guild.id)
        # df = pd.read_csv('./data/guild_id_list.csv')
        df = pd.DataFrame(self.guild_id_list, index=None, columns=None) 
        print(df)
        df.to_csv('./data/guild_id_list.csv', index=None, header=False)

        @commands.Cog.listener()
        async def on_guild_remove(self, guild):
            pass
            

def setup(bot):
    return bot.add_cog(SortRiddleCog(bot))
