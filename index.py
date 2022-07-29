import discord
from discord.ext import commands
import os
import json
from pymongo import MongoClient

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("<", "93 "),
    case_insensitive=True,
    owner_id=800428078308392996,
    intents=intents)

client.remove_command('help')

uri = 'mongodb+srv://riju:1234@cluster0.csdbd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
cluster = MongoClient(uri)
db = cluster['servers']
col_ig = db['servers']

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

for filename in os.listdir('./subcogs'):
    if filename.endswith('.py'):
        client.load_extension(f"subcogs.{filename[:-3]}")


async def get_afk_data():
    with open("./storage/afk.json", "r") as f:
        users = json.load(f)

    return users


@client.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(client.user))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.guild:
        return

    ch_id = str(message.channel.id)

    checks = col_ig.find({ch_id: True})

    items = []

    for check in checks:
        for key in check:
            items.append(key)

    if ch_id in items:
        return

    users = await get_afk_data()

    userid = str(message.author.id)

    if userid in users:
        del users[userid]

        with open("./storage/afk.json", "w") as f:
            json.dump(users, f)

        e = discord.Embed(
            description=f"Welcome back {message.author.display_name}, afk status has been reset",
        )

        await message.reply(embed=e, mention_author=False)

    for x in users:
        if x in message.content.lower():
            member = client.get_user(int(x))
            name = member.name

            e = discord.Embed(
                description=f"{message.author.mention} {name} is afk — {users[x]['status']}",
            )

            await message.reply(embed=e, mention_author=False)

    await client.process_commands(message)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.reply(embed=discord.Embed(description=f"Loaded extension {extension}"), mention_author=False)


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.reply(embed=discord.Embed(description=f"Unoaded extension {extension}"), mention_author=False)


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.reply(embed=discord.Embed(description=f"Reloaded extension {extension}"), mention_author=False)


client.run('Nzg0NzY4ODAyMjAxMDEwMTk4.GQeufg.z2vJ640Aj5lHnvghiatG1u8eq9daZM3_FgJRDA')