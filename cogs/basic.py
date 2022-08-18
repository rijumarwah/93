import discord
from discord.ext import commands
import datetime, time


start_time = time.time()


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(
        aliases=['latency'],
        usage="<ping",
        brief="Returns the bot's latency",
    )
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send(":ping_pong: Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.delete()
        await ctx.send(content=f":ping_pong: Pong! {round(int(ping))}ms")


    @commands.command(
        aliases=['prefixes'],
        usage='<prefix',
        brief="Returns the bot's prefixes"
    )
    async def prefix(self, ctx):
        await ctx.reply(embed=discord.Embed(description="My Prefixes: `<`, `93`, `@93`"), mention_author=False)


    @commands.command(
        aliases=['add'],
        usage="<invite",
        brief="Returns an invite for the bot",
    )
    async def invite(self, ctx):
        await ctx.reply(embed=discord.Embed(description="You can invite me using this hyperlink [Invite](https://discord.com/oauth2/authorize?client_id=718749763859775559&permissions=8&scope=bot)", color=0x2f3136), mention_author=False)


    @commands.command(
        usage='<friends',
        brief='Other bots from my devs'
    )
    async def friends(self, ctx):
        await ctx.reply(embed=discord.Embed(title="Other bots created by devs at Aizor Studio", description="Akinator: [Invite](https://discord.com/api/oauth2/authorize?client_id=804789290139385887&permissions=20278592&scope=bot%20applications.commands)\n24/7 Music: [Invite](https://discord.com/oauth2/authorize?client_id=784807517334011934&permissions=62380864&scope=bot%20applications.commands)\nKasumi Music: [Invite](https://discord.com/oauth2/authorize?client_id=768155743819399169&permissions=8&scope=applications.commands%20bot)"), mention_author=False)


    @commands.command(
        usage='<stats',
        brief="Returns basic bot stats"
    )
    async def stats(self, ctx):
        e = discord.Embed(
            color=0x2f3136,
            description=f"Connected on {len(self.client.guilds)} servers with over {len(self.client.users)} users"
        )

        await ctx.reply(embed=e, mention_author=False)

            
    @commands.command(
        usage='<support',
        brief='Return an invite for my support guild'
    )
    async def support(self, ctx):
        await ctx.reply(embed=discord.Embed(description=f"Join my Support Guild: [https://discord.gg/aRSUD2dn7E](https://discord.gg/aRSUD2dn7E)"), mention_author=False)
        
        
def setup(client):
    client.add_cog(Basic(client))
