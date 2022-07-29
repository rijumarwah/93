import discord
from discord.ext import commands
import asyncio
import requests
import random
import re
import io
from io import StringIO
import PIL
from PIL import Image
from pymongo import MongoClient
import json


uri = "mongodb+srv://riju:1234@cluster0.2iy0s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["todo"]
col = db["todo"]


def new_user(u_id):
    post = {"user": u_id}
    col.insert_one(post)


def add_array(u_id):
    q = {'user': u_id}
    values = {'$set': {'do': []}}

    col.update_one(q, values)


def add_task(u_id, task):
    query = {'user': u_id}
    col.update(query, {'$push': {'do': task}})


def add_task_done(u_id, task):
    query = {'user': u_id}
    col.update(query, {'$push': {'done': task}})


def remove_task(u_id, index):
    query = {'user': u_id}
    for x in col.find(query):
        doc = x

    item = doc['do'][index]
    col.update(query, {'$pull': {'do': {item}}})


def task_list(u_id):
    query = {'user': u_id}
    for x in col.find(query):
        return x


time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


async def get_afk_data():
    with open("./storage/afk.json", "r") as f:
        users = json.load(f)

    return users


def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)


def read_json(filename):
	with open(f"{filename}.json", "r") as file:
		data = json.load(file)
	return data


def write_json(data, filename):
	with open(f"{filename}.json", "w") as file:
		json.dump(data, file, indent=4)


async def get_afk_data():
	with open("./storage/afk.json", "r") as f:
		users = json.load(f)

	return users


class Utility(commands.Cog):
    """Utility Commands"""

    def __init__(self, client):
        self.client = client

    
    @commands.group(
        aliases=['setafk', 'away'],
        usage='<afk [status/none]',
        brief='Sets a status for you while away'
    )
    async def afk(self, ctx, *, status=None):

        if not status:
            status = 'Not specified'

        users = await get_afk_data()

        if not ctx.author.id in users:
            users[str(ctx.author.id)] = {}
            users[str(ctx.author.id)]['status'] = status

        else:
            users[str(ctx.author.id)]['status'] = status

        with open("./storage/afk.json", "w") as f:
            json.dump(users, f)
        

        await ctx.reply(embed=discord.Embed(description=f"Your afk status has been set to '{status}'"), mention_author=False)


    @commands.command(
        aliases=['exp', 'e'],
        usage='<expand [custom emote]',
        brief='Returns an enlarged version of the emote'
    )
    async def expand(self, ctx, emoji: discord.PartialEmoji=None):

        if not emoji:
            return await ctx.reply("You didn't provide a custom emote", mention_author=False)

        await ctx.reply(f"{emoji.url}", mention_author=False)


    @commands.command(
        aliases=['av', 'avy'],
        usage='<avatar [user/none]',
        brief='Returns user\'s avatar'
    )
    async def avatar(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        uri = str(member.avatar_url)

        uri = uri.replace('size=1024', 'size=256')
            
        e = discord.Embed()
        e.set_image(url=uri)
        e.set_author(name=f"{member}", icon_url=member.avatar_url)

        await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        usage='<archive [amount]',
        brief='Create a chat archive'
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def archive(self, ctx, limit=50):
        if limit > 2500:
            await ctx.reply(f"Too many messages (>2500)")
            return

        counter = 0
        msgs = []
        async for message in ctx.channel.history(limit=limit):
            try:
                msgs.append(f"[{str(message.created_at)[:-7]}] - {message.author} -> {message.content}\n")
            except:
                pass
            counter += 1

        file = io.open("./storage/archive.txt", "w", encoding="utf-8")
        file.writelines(msgs)

        if len(msgs) == 0:
            await ctx.reply(f"No messages found", mention_author=False)
        else:
            file = discord.File("./storage/archive.txt", filename="archive.txt")
            await ctx.reply(f"I archived {len(msgs)} messages that I could access", file=file, mention_author=False)


    @commands.command(
        usage='<weather [location]',
        brief="Returns various info for the weather"
    )
    async def weather(self, ctx, *, query=None):

        if not query:
          await ctx.reply(f'You did not tell me what location to search the weather for', mention_author=False)
          return

        try:

            querya = query.replace(" ", "+")

            api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=6106f39f370b92d9491bfc26e5df4f3e&q='

            url = api_address + querya

            json_data = requests.get(url).json()

            weather_t = json_data['weather'][0]['main']

            temp = json_data['main']['temp']

            temp_c = (int(temp) - 273.15)

            temp_f = (temp_c * 9 / 5) + 32

            windspeed = json_data['wind']['speed']

            feels_like = json_data['main']['feels_like']

            feels_like = round(int(feels_like) - 273.15)

            temp_min = json_data['main']['temp_min']
            temp_min_c = (int(temp_min) - 273.15)

            temp_max = json_data['main']['temp_max']
            temp_max_c = (int(temp_max) - 273.15)

            pressure = json_data['main']['pressure']

            humidity = json_data['main']['humidity']

            loc_c = json_data['sys']['country']

            loc_p = json_data['name']

            visibility = json_data['visibility']

            lat = json_data['coord']['lat']

            lon = json_data['coord']['lon']

            embed = discord.Embed(

            )

            embed.set_author(name=f"Weather — {loc_p}, {loc_c}", icon_url='https://i.imgur.com/CpbNTYM.gif')


            embed.add_field(name=':cloud: Weather', value=f"{weather_t}",
                            inline=True)
            embed.add_field(name=':sweat: Humidity',
                            value=f"{humidity}%",
                            inline=True)
            embed.add_field(name=":thermometer: Temperature", value=f"{round(temp_f, 2)}°F/{round(temp_c, 2)}°C",
                            inline=True)
            embed.add_field(name=":white_sun_small_cloud: Feels Like", value=f"{feels_like}°C",
                            inline=True)
            embed.add_field(name=':dash: Wind Speed',
                            value=f"{windspeed}mph",
                            inline=True)
            embed.add_field(name=":eyes: Visibility",
                            value=f"{visibility}m",
                            inline=True)
            embed.add_field(name=":straight_ruler: Lat/Long",
                            value=f"{lat}/{lon}",
                            inline=True)
            embed.add_field(name=":high_brightness: Min/Max",
                            value=f"{round(temp_min_c, 1)}°C/{round(temp_max_c, 1)}°C",
                            inline=True)
            embed.add_field(name=":anger: Pressure",
                            value=f"{pressure}hPa",
                            inline=True)

            await ctx.reply(embed=embed, mention_author=False)

        except:
            em = discord.Embed(
                description="Location not found"
            )

            await ctx.reply(embed=em, mention_author=False)

        
    @commands.command(
        usage='<timer [time]',
        brief="Sets a timer "
    )
    async def timer(self, ctx, arg):
        await ctx.reply(f"Ok, I have set the timer", mention_author=False)

        amount = convert(arg)

        await asyncio.sleep(amount)

        em = discord.Embed(description=f"Time up! {amount}")
        em.set_author(name="Timer", icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=em)


    @commands.command(
        usage='<choose [option;option]',
        brief="Randomly chooses out of options"
    )
    async def choose(self, ctx, *choices):
        string = " ".join(choices)

        string = string.split(';')

        await ctx.reply(f"{ctx.author.mention} I would choose: {random.choice(string)}", mention_author=False)


    @commands.command(
        usage='<remind [time] [reminder]',
        brief="Sets a reminder for you"
    )
    async def remind(self, ctx, time, *, reminder):
        time = convert(time)

        await ctx.reply(f"Ok, I will remind you", mention_author=False)
        await asyncio.sleep(time)

        e = discord.Embed(description=f"{reminder}")
        e.set_author(name="Event Reminder", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        usage='<flip [times]',
        brief="Flip a coin"
    )
    async def flip(self, ctx, coins=None):
    
        choice = ['h', 't']
    
        if not coins:
            ch = random.choice(choice)
            if ch == "t":
                text = "Heads!"
            else:
                text = "Tails!"
    
            await ctx.reply(text, mention_author=False)
            return
    
        try:
            coins = int(coins)
    
            if coins >= 1000:
                await ctx.reply("Too many coins >1000", mention_author=False)
    
            elif coins < 2:
                await ctx.reply("Choose more than 2 coins", mention_author=False)
    
            else:
                flips = []
    
                for i in range(coins):
                    ch = random.choice(choice)
                    flips.append(ch)
    
                count_h = flips.count('h')
                count_t = flips.count('t')
    
                await ctx.reply(f"Heads: {count_h}\nTails: {count_t}", mention_author=False)
    
        except:
            await ctx.reply("Invalid format. Usage: `<flip [number of coins]`", mention_author=False)


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def poll(self, ctx, *, message=None):

        if not message:
            return await ctx.reply("You need to tell me what the poll content should be `<poll [am i stupid]`", mention_author=False)

        await ctx.message.delete()

        em = discord.Embed(description=f"Enter type of poll: [1] Yes/No [2] Multiple Choice")
        em.set_author(name="Poll type", icon_url=ctx.author.avatar_url)
        first = await ctx.send(embed=em)
        ida = await self.client.wait_for('message', check=check(ctx.author), timeout=20)
        content = ida.content
        content = str(content)

        await ida.delete()
        await first.delete()

        if content == "1":
            em = discord.Embed(title="📢 Poll", description=f"{message}")
            em.set_footer(text=f"Poll started by {ctx.author}", icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=em)

            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

        elif content == "2":

            reacts = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

            emx = discord.Embed(description=f"Enter options, each separated by a `;` (maximum choices: 9)")
            emx.set_author(name="Enter options", icon_url=ctx.author.avatar_url)
            second = await ctx.send(embed=emx)
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=60)
            content = ida.content
            content = str(content)
            
            await ida.delete()
            await second.delete()

            options = content.split(";")
            if len(options) > 9:
                await ctx.send(f"Max options supported: 9")
            else:
                em = discord.Embed(title="📢 Poll", description=f"{message}")
                em.set_footer(text=f"Poll started by {ctx.author}", icon_url=ctx.author.avatar_url)
                for i in range(len(options)):
                    em.add_field(name=f"{reacts[i]}", value=f"{options[i]}", inline=False)
                msg = await ctx.send(embed=em)
                for j in range(len(options)):
                    await msg.add_reaction(f"{reacts[j]}")
        else:
            await ctx.send(f"Choice incorrectly entered")


    @commands.command(
        usage='<color [hex code]',
        brief="Returns an image preview for the hex"
    )
    async def color(self, ctx, hex: str = None):
        if not hex:
            await ctx.send("No hex provided")

        hex = hex.replace('#', '')

        url = "https://some-random-api.ml/canvas/colorviewer?hex=" + hex

        r = requests.request('GET', url)

        with open('./storage/color.png', 'wb') as f:
            for chunk in r:
                f.write(chunk)

        im = Image.open('./storage/color.png')

        new_image = im.resize((64,64))

        new_image.save('./storage/color.png')


        file = discord.File("./storage/color.png", filename="color.png")
        await ctx.reply(file=file, mention_author=False)

    
    @commands.group(
        usage='<todo [category]',
        brief='Todo list'
    )
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(embed=discord.Embed(description="Todo list commands: `<todo add`, `<todo remove`, `<todo list`"), mention_author=False)


    @todo.command(
        aliases=['task', 'new'],
        usage='<todo add [task]',
        brief='Add task to ToDo list'
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, *, task: str=None):

        if ctx.invoked_subcommand is None:

            if not task:
                e = discord.Embed(
                    description="Usage: `todo add [task]`"
                )

                await ctx.reply(embed=e, mention_author=False)
                return

            if len(task) > 250:
                await ctx.reply("Task cannot contain more than 250 characters", mention_author=False)
                return

            user = ctx.author.id

            if col.count({'user': user}) == 0:
                new_user(user)

            add_task(user, task)

            await ctx.reply("Added task", mention_author=False)


    @todo.command(
        aliases=['done'],
        usage='<todo remove [index]',
        brief="Remove ToDo list task"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove(self, ctx, index=None):

        if ctx.invoked_subcommand is None:

            if not index:
                u_id = ctx.author.id

                query = {'user': u_id}
                for x in col.find(query):
                    doc = x

                dos = doc['do']

                li = []

                for i in range(len(dos)):
                    li.append(f"{i+1}: {dos[i]}")

                mes = '\n'.join(li)

                e = discord.Embed(
                    description=f"{mes}"
                )

                e.set_author(name="Removable Tasks", icon_url=ctx.author.avatar_url)
                e.set_footer(text="todo remove [index] to remove a task")

                await ctx.reply(embed=e, mention_author=False)
            
            else:
                try:
                    u_id = ctx.author.id

                    query = {'user': u_id}
                    for x in col.find(query):
                        doc = x

                    dos = doc['do']

                    dos.pop(int(index)-1)

                    q = {'user': u_id}
                    values = {'$set': {'do': dos}}

                    col.update_one(q, values)

                    await ctx.reply("Removed task", mention_author=False)

                except:
                    await ctx.reply("Index out of range", mention_author=False)


    @todo.command(
        aliases=['all'],
        usage='<todo list',
        brief="Returns ToDo list"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list(self, ctx):

        if ctx.invoked_subcommand is None:

            user = ctx.author.id

            if col.count({'user': user}) == 0:
                await ctx.reply("You have no tasks in your list", mention_author=False)

            else:

                x = dict(task_list(user))

                if len(x['do']) == 0:
                    await ctx.reply("You have no tasks in your list", mention_author=False)
                    return

                tasks_do = f'\n- '.join(x['do'])
                tasks_do = '- ' + tasks_do

                if len(tasks_do) > 2000:
                    tasks_do[:2000] + ...

                e = discord.Embed(
                    description=f"{tasks_do}"
                )

                e.set_author(name=f"{ctx.author.display_name}'s Todo List", icon_url=ctx.author.avatar_url)

                await ctx.reply(embed=e, mention_author=False)

    
    @commands.command(
        aliases=['q'],
        brief='Quotes a message by id',
        usage='<quote [message id]'
    )
    async def quote(self, ctx, m: discord.Message=None):
        if not m:
            return await ctx.reply('You didn\'t tell me what message to quote (use message id)', mention_author=False)
        
        e = discord.Embed(
            description=f"{m.content}\n\n[Jump to original message]({m.jump_url})", timestamp=m.created_at
        )
        
        e.set_author(name=f"{m.author}", icon_url=f"{m.author.avatar_url}")

        if len(m.attachments) > 0:
            e.set_image(url=f"{m.attachments[0].url}")
        
        e.set_footer(text=f"#{m.channel}")
        
        await ctx.reply(embed=e, mention_author=False)


def setup(client):
    client.add_cog(Utility(client))
