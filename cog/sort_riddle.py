import bisect
import json
import requests
import time
import datetime

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
    async def neko(self, ctx):
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

        bisect.insort(self.guild_id_list, guild.id)
        # df = pd.read_csv('./data/guild_id_list.csv')
        df = pd.DataFrame(self.guild_id_list, index=None, columns=None)
        print(df)
        df.to_csv('./data/guild_id_list.csv', index=None, header=False)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        to_delete_index = bisect.bisect(self.guild_id_list, guild.id)

        self.sort_riddle_data.pop(to_delete_index)
        with open('./data/sort_riddle_data.json', 'w') as f:
            json.dump(self.sort_riddle_data, f, indent=4)

        self.guild_id_list.pop(guild.id)
        df = pd.DataFrame(self.guild_id_list, index=None, columns=None)
        df.to_csv('./data/guild_id_list.csv', index=None, header=False)

    @commands.command()
    async def start(self, ctx):
        index = bisect.bisect(self.guild_id_list, ctx.author.guild.id)
        if index is None:
            await ctx.send('guild id が存在してないにゃ')
            return

        if q := self.sort_riddle_data[index]['question'] is not None:
            await ctx.send(f'問題は **{q}** だにゃ')
            return

        link = 'https://ja.wikipedia.org/w/api.php?action=query&list=random&format=json'
        response = requests.get(link)
        json_data = response.json()

        """
        json_data
        {'batchcomplete': '',
            'continue': {'continue': '-||',
                        'rncontinue': '0.269787212577|0.269787813864|1126887|0'},
            'query': {'random': [{'id': 2226876,
                                'ns': 10,
                                'title': 'Template:Country alias 岐阜県'}]}}
        """

        a = json_data['query']['random'][0]['title'].replace(' ', '_')
        self.sort_riddle_data[index]['answer'] = a
        q = ''.join(sorted(list(a)))
        self.sort_riddle_data[index]['quetion'] = q
        await ctx.send(f'問題は**{q}**だにゃ')

        self.sort_riddle_data[index]['start_time'] = time.time()
        # 諸々を書き込み
        with open('./data/sort_riddle_data.json', 'w') as f:
            json.dump(self.sort_riddle_data, f, indent=4)

    @commands.command()
    async def answer(self, ctx, answer: str):
        # questionが存在するかチェック
        index = bisect.bisect(self.guild_id_list, ctx.author.guild.id)
        q = self.sort_riddle_data[index]['question']
        if q is not None:
            await ctx.send(f'{ctx.author.mention} **/start** と入力してにゃ')
            return
        # 長さがあってるかチェック
        if len(q) != len(answer):
            await ctx.send(f'{ctx.author.mention} ぶっぶー！長さが違うにゃ')
            return
        # 正誤判定
        cnt = 0
        for i in range(len(q)):
            if q[i] == answer[i]:
                cnt += 1
        if cnt == len(answer):
            correct_time = time.time()
            td = datetime.timedelta(seconds=self.sort_riddle_data[index]["start_time"] - correct_time)
            await ctx.send(f'{ctx.author.mention} 正解だにゃ\n クリア時間は{td}だにゃ \
            \nhttps://ja.wikipedia.org/wiki/{q}')
            # answer, question, start_time を消去
            self.sort_riddle_data[index]['answer'] = None
            self.sort_riddle_data[index]['question'] = None
            self.sort_riddle_data[index]['start_time'] = None
            with open('./data/sort_riddle_data.json', 'w') as f:
                json.dump(self.sort_riddle_data, f, indent=4)
        else:
            await ctx.send(f'{ctx.author.mention} ぶっぶー！ **{cnt}**文字あってるにゃ')

    @commands.command()
    async def help(self, ctx):
        index = bisect.bisect(self.guild_id_list, ctx.author.guild.id)
        a = self.sort_riddle_data[index]['answer']
        if a is None:
            await ctx.send(f'{ctx.author.mention} **/start** と入力してにゃ')
            return
        await ctx.send(f'最初の文字は **{a[0]}** だにゃ')

    @commands.command()
    async def giveup(self, ctx):
        index = bisect.bisect(self.guild_id_list, ctx.author.guild.id)
        a = self.sort_riddle_data[index]['answer']
        if a is None:
            await ctx.send(f'{ctx.author.mention} **/start** と入力してにゃ')
            return

        await ctx.send(f'わからないのかにゃ？ 答えは **{a}** だにゃ\nhttps://ja.wikipedia.org/wiki/{a}')
        
        # answer, question, start_time を消去
        self.sort_riddle_data[index]['answer'] = None
        self.sort_riddle_data[index]['question'] = None
        self.sort_riddle_data[index]['start_time'] = None
        with open('./data/sort_riddle_data.json', 'w') as f:
            json.dump(self.sort_riddle_data, f, indent=4)

def setup(bot):
    return bot.add_cog(SortRiddleCog(bot))
