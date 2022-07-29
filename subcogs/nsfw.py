import discord
from discord.ext import commands
import json
import requests


class Nsfw(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nsfw(self, ctx):
        await ctx.send(embed=discord.Embed(description="hey you can use one of these in a nsfw channel: hentaigif, neko, lesbain, boobs, hentai, lewdk, pussy, yuri, lewd, anal, waifu, tits, classic"))

    @commands.command()
    async def hentaigif(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/Random_hentai_gif"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Hentai GIF"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def neko(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/neko"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Neko"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def lesbian(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/les"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Lesbo"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def boobs(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/boobs"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Boobs"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def hentai(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/hentai"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Hentai"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def lewdk(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/lewdk"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Lewdk"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def pussy(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/pussy_jpg"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Pussy"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def yuri(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/yuri"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Yuri"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def lewd(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/lewd"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Lewd"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def anal(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/anal"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Anal"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def waifu(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/waifu"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Waifu"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def tits(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/tits"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="Tits"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def classic(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send(":underage: NSFW text channels only")

        else:
            url = "https://nekos.life/api/v2/img/classic"

            r = requests.request('GET', url).json()

            try:
                em = discord.Embed(
                    title="The classics"
                )

                em.set_image(url=f"{r['url']}")

                await ctx.send(embed=em)

            except:
                await ctx.send("API error")


    @commands.command()
    async def owoify(self, ctx, *, text: str):
        url = "https://nekos.life/api/v2/owoify?text=" + text

        r = requests.request('GET', url).json()

        try:

            em = discord.Embed(
                description=f"{r['owo']}",
            )

            await ctx.send(embed=em)

        except:
            await ctx.send("API error")

        
def setup(client):
    client.add_cog(Nsfw(client))
