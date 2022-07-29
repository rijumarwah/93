import discord
from discord.ext import commands
from pymongo import MongoClient


uri_ig = 'mongodb+srv://riju:1234@cluster0.csdbd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

cluster_ig = MongoClient(uri_ig)
db_ig = cluster_ig['servers']
col_ig = db_ig['servers']


class Automsg(commands.Cog):
    """Auto Message Category"""

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):

        g_id = str(member.guild.id)

        results = col_ig.find({'welcome': True})
        checks = col_ig.find({'welcome': True})
        
        items = []

        for check in checks:
            for key in check:
                items.append(key)
        
        if not g_id in items:
            return

        for value in items:
            for result in results:
                channel_id = result[g_id]

        cha = self.client.get_channel(channel_id)

        e = discord.Embed(
            color=0xd6f5ff,
            description=f"Member count for the guild is now {member.guild.member_count}\nAccount ID: {member.id}"
        )

        e.set_author(icon_url=member.avatar_url, name=f'Welcome to the guild {member.name}!')
        
        e.set_thumbnail(url=member.avatar_url)

        await cha.send(embed=e)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        
        g_id = str(member.guild.id)

        results = col_ig.find({'goodbye': True})
        checks = col_ig.find({'goodbye': True})
        
        items = []

        for check in checks:
            for key in check:
                items.append(key)
        
        if not g_id in items:
            return

        for value in items:
            for result in results:
                channel_id = result[g_id]

        cha = self.client.get_channel(channel_id)

        e = discord.Embed(
            color=0xc7c7c7,
            description=f"Member count for the guild is now {member.guild.member_count}\nAccount ID: {member.id}"
        )

        e.set_author(icon_url=member.avatar_url, name=f'{member.name} left the guild')
        
        e.set_thumbnail(url=member.avatar_url)

        try:
            await cha.send(embed=e)
        except:
            return


def setup(client):
    client.add_cog(Automsg(client))