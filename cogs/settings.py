import discord
from discord.ext import commands
from pymongo import MongoClient

uri_ig = 'mongodb+srv://riju:1234@cluster0.csdbd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

cluster_ig = MongoClient(uri_ig)
db_ig = cluster_ig['servers']
col_ig = db_ig['servers']


class Settings(commands.Cog):
    """Settings Commands"""

    def __init__(self, client):
        self.client = client


    @commands.command(
        usage='<ignore [text channel]',
        brief="Make me ignore certain text channels"
    )
    @commands.has_permissions(manage_guild=True)
    async def ignore(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            return await ctx.reply("You didnt tell me what channel to ignore", mention_author=False)

        ch_id = str(channel.id)

        checks = col_ig.find({ch_id: True})
        
        items = []

        for check in checks:
            for key in check:
                items.append(key)

        
        if ch_id in items:
            return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} has already been added to my ignore list"), mention_author=False)


        try:
            q = {'ignore': True}
            v = {'$set': {ch_id: True}}

            col_ig.update_one(q, v)

            await ctx.reply(embed=discord.Embed(description=f"I will no longer respond in {channel.mention}. Do `<unignore [channel]` to revert this"), mention_author=False)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"An error occured: {e}"), mention_author=False)


    @commands.command(
        usage='<unignore [text channel]',
        brief="Make me respond in ignored text channels"
    )
    @commands.has_permissions(manage_guild=True)
    async def unignore(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            return await ctx.reply("You didnt tell me what channel to unignore", mention_author=False)

        ch_id = str(channel.id)

        checks = col_ig.find({ch_id: True})
        
        items = []

        for check in checks:
            for key in check:
                items.append(key)

        
        if ch_id not in items:
            return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} has not been added to my ignore list yet"))


        try:
            col_ig.update({'ignore': True}, {"$unset": {ch_id : 1}}, False, True)

            await ctx.reply(embed=discord.Embed(description=f"I will now respond in {channel.mention}. Do `<ignore [channel]` to revert this"), mention_author=False)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"An error occured: {e}"), mention_author=False)


    @commands.command(
        usage='<setwelcome [channel id]',
        brief='Makes the bot send a welcome message'
    )
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            return await ctx.reply(embed=discord.Embed(description="You need to provide the channel parameter, where you want me to send welcome messages"), mention_author=False)

        g_id = str(ctx.guild.id)

        results = col_ig.find({'welcome': True})
        checks = col_ig.find({'welcome': True})

        items = []

        for check in checks:
            for key in check:
                items.append(key)

        if g_id in items:
            return await ctx.reply(embed=discord.Embed(description=f"Welcome message channel already set. Use `<removewelcome` to disable"), mention_author=False)

        try:
            q = {'welcome': True}
            v = {'$set': {g_id: channel.id}}

            col_ig.update_one(q, v)

            await ctx.reply(embed=discord.Embed(description=f"Welcome messages set to be sent in {channel.mention}"), mention_author=False)
        
        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"An error occured: {e}"), mention_author=False)


    @commands.command(
        usage='<setleave [channel id]',
        brief='Makes the bot send a goodbye message'
    )
    @commands.has_permissions(manage_guild=True)
    async def setleave(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            return await ctx.reply(embed=discord.Embed(description="You need to provide the channel parameter, where you want me to send leave messages"), mention_author=False)

        g_id = str(ctx.guild.id)

        results = col_ig.find({'goodbye': True})
        checks = col_ig.find({'goodbye': True})

        items = []

        for check in checks:
            for key in check:
                items.append(key)

        if g_id in items:
            return await ctx.reply(embed=discord.Embed(description=f"Leave message channel already set. Use `<removeleave` to disable"), mention_author=False)

        try:
            q = {'goodbye': True}
            v = {'$set': {g_id: channel.id}}

            col_ig.update_one(q, v)

            await ctx.reply(embed=discord.Embed(description=f"Goodbye messages set to be sent in {channel.mention}"), mention_author=False)
        
        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"An error occured: {e}"), mention_author=False)


    @commands.command(
        usage='<removewelcome',
        brief="Removed the welcome auto message"
    )
    @commands.has_permissions(manage_guild=True)
    async def removewelcome(self, ctx):
        g_id = str(ctx.guild.id)

        results = col_ig.find({'welcome': True})
        checks = col_ig.find({'welcome': True})

        items = []

        for check in checks:
            for key in check:
                items.append(key)

        if not g_id in items:
            return await ctx.reply(embed=discord.Embed("Welcome message has not been set"), mention_author=False)

        try:
            col_ig.update({'welcome': True}, {"$unset": {g_id : 1}}, False, True)
            await ctx.reply(embed=discord.Embed(description="Disabled welcome auto message"), mention_author=False)
        except:
            await ctx.reply(embed=discord.Embed(description="Something went wrong"), mention_author=False)


    @commands.command(
        usage='<removeleave',
        brief="Removed the leave auto message"
    )
    @commands.has_permissions(manage_guild=True)
    async def removeleave(self, ctx):
        g_id = str(ctx.guild.id)

        results = col_ig.find({'goodbye': True})
        checks = col_ig.find({'goodbye': True})

        items = []

        for check in checks:
            for key in check:
                items.append(key)

        if not g_id in items:
            return await ctx.reply(embed=discord.Embed("Leave message has not been set"), mention_author=False)

        try:
            col_ig.update({'goodbye': True}, {"$unset": {g_id : 1}}, False, True)
            await ctx.reply(embed=discord.Embed(description="Disabled leave auto message"), mention_author=False)
        except:
            await ctx.reply(embed=discord.Embed(description="Something went wrong"), mention_author=False)


def setup(client):
    client.add_cog(Settings(client))