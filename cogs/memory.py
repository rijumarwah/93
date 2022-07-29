import discord
from discord.ext import commands
from pymongo import MongoClient
import asyncio

uri1 = "mongodb+srv://riju:1234@cluster0.owqch.mongodb.net/93?retryWrites=true&w=majority"

cluster1 = MongoClient(uri1)
db1 = cluster1["93"]
col1 = db1["tags"]


uri2 = "mongodb+srv://riju:1234@cluster0.nblcd.mongodb.net/profiles?retryWrites=true&w=majority"

cluster2 = MongoClient(uri2)
db2 = cluster2["93"]
col2 = db2["tags"]


def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Memory(commands.Cog):
    """Memory Commands"""

    def __init__(self, client):
        self.client = client


    @commands.command(
        usage='<tag [name]',
        brief="Call out a tag you made"
    )
    async def tag(self, ctx, *, name=None):
        if not name:
            return await ctx.reply(embed=discord.Embed(description="You didn't give me a tag name to look for"), mention_author=False)

        userid = str(ctx.author.id)
        results = col1.find({"userid": userid})

        checks = col1.find({'userid': userid})

        items = []

        for check in checks:
            for key in check:
                items.append(key)


        if name in items:
            for result in results:
                await ctx.reply(result[name], mention_author=False)

        else:
            await ctx.reply(embed=discord.Embed(description=f"I couldn't find a tag named '{name}'"), mention_author=False)


    @commands.command(
        aliases=['ctag'],
        usage='<createtag [name] [value]',
        brief='Create a personal tag'
    )
    async def createtag(self, ctx, name=None, *, value=" "):
        if ctx.invoked_subcommand is None:
            if not name:
                return await ctx.reply("You didn't give me a tag name", mention_author=False)

            if '@everyone' in value or '@here' in value:
                return await ctx.reply("You cannot have mentions in tag values", mention_author=False)

            if len(value) > 500:
                return await ctx.reply("Tag values should be under 500 characters", mention_author=False)


            # -------

            if len(ctx.message.attachments) > 0:
                attach_link = ctx.message.attachments[0].url
                value = value + attach_link


            userid = str(ctx.author.id)

            if col1.count({'userid': userid}) != 0:
                checks = col1.find({'userid': userid})

                items = []

                for check in checks:
                    for key in check:
                        items.append(key)

                if name in items:
                    return await ctx.reply(embed=discord.Embed(description=f"You already have a tag named '{name}'"), mention_author=False)

                try:
                    myquery = {"userid": userid}
                    newvalues = {"$set": {name: value}}

                    col1.update_one(myquery, newvalues)
                    await ctx.reply(embed=discord.Embed(description=f"Added tag '{name}' to your account"), mention_author=False)

                except Exception as e:
                    await ctx.reply(embed=discord.Embed(f"Something went wrong, {e}"), mention_author=False)

            else:
                post = {"userid": userid, name: value}
                col1.insert_one(post)
                await ctx.reply(embed=discord.Embed(description=f"Your account was created, and tag '{name}' was added"), mention_author=False)


    @commands.command(
        aliases=['tagdelete', 'tagdel', 'deltag', 'dtag'],
        usage='<deletetag [name]',
        brief="Delete an existing tag"
    )
    async def deletetag(self, ctx, *, name=None):
        if not name:
            return await ctx.reply(embed=discord.Embedd(description="You didn't tell me what tag to delete"), mention_author=False)

        checks = col1.find({'userid' : str(ctx.author.id)})

        items = []

        for check in checks:
            for key in check:
                items.append(key)

        if name in items:
            col1.update({'userid' : str(ctx.author.id)}, {"$unset" : {name : 1}}, False, True)
            await ctx.reply(embed=discord.Embed(description=f"Deleted tag '{name}'"), mention_author=False)

        else:
            await ctx.reply(embed=discord.Embed(description=f"I couldn't find a tag named '{name}' registered"), mention_author=False)


    @commands.command(
        usage='<alltags',
        brief="Returns a list of all your tags"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def alltags(self, ctx):
        async with ctx.channel.typing():

            results = col1.find({"userid" : str(ctx.author.id)})

            result_ = []

            for result in results:
                for name in result:
                    result_.append(name)

            result_.pop(0)
            result_.pop(0)

            if len(result_) == 0:
                return await ctx.reply("You have no tags", mention_author=False)

            if len(result_) < 11:
                des = '\n'.join(result_)
                try:
                    await ctx.reply('Tags sent on direct messages', mention_author=False)
                    return await ctx.author.send(embed=discord.Embed(title=f"{ctx.author}'s tags", description=des))

                except:
                    await ctx.reply('Can\'t send direct messages to you', mention_author=False)


            res = list(chunks(result_, 10))

            pages = []

            count = 1

            for i in res:
                des = '\n'.join(i)

                pages.append(discord.Embed(title=f"{ctx.author}'s tags", description=des).set_footer(text=f"Page {count}/{len(res)}"))

                count += 1

            buttons = ['◀', '▶', '🗑']

        try:
            m = await ctx.author.send(embed=pages[0])

        except:
            return await ctx.reply("Can't send the direct message, you would have to allow direct messages from guild members in order for this to work", mention_author=False)

        await ctx.reply(embed=discord.Embed(description="Hey check your direct messages"), mention_author=False)

        for reaction in buttons:
            await m.add_reaction(reaction)


        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in buttons


        page_track = 0


        while True:

                try:

                    reaction, user = await self.client.wait_for('reaction_add', timeout=60, check=check)

                    if reaction.emoji == buttons[0]:
                        if page_track != 0:
                            page_track -= 1
                            await m.edit(embed=pages[page_track])

                        else:
                            pass


                    if reaction.emoji == buttons[1]:
                        if page_track < len(pages) - 1:
                            page_track += 1
                            await m.edit(embed=pages[page_track])

                        else:
                            pass


                    elif reaction.emoji == buttons[2]:
                        await m.remove_reaction(buttons[0], self.client.user)
                        await m.remove_reaction(buttons[1], self.client.user)
                        await m.remove_reaction(buttons[2], self.client.user)
                        return

                except asyncio.TimeoutError:
                    await m.remove_reaction(buttons[0], self.client.user)
                    await m.remove_reaction(buttons[1], self.client.user)
                    await m.remove_reaction(buttons[2], self.client.user)
                    return

                except Exception as e:
                    await ctx.send(e)
                    return


    @commands.group(
        usage='<profile [category]',
        brief="Sets a custom profile"
    )
    async def profile(self, ctx):
        if ctx.invoked_subcommand is None:

            em = discord.Embed(description="""
`<profile view [user/none]` - View user's profile
`<profile set` - Setup profile 
`<profile delete` - Reset your profile
`<profile connect [service name] [account name] [link (optional)]` - Add a connection
`<profile xconnect` - Remove a connection
`<profile follow [user]` - Follow a user
`<cookie [user]` - Send cookies
"""
            )

            em.set_author(name="Profile Commands", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=em)




    @profile.command(
        usage='<profile view [member/none]',
        brief="Lets you view a member's profile"
    )
    async def view(self, ctx, member: discord.Member = None):
        if ctx.invoked_subcommand is None:
            if not member:
                member = ctx.author
                userid = str(ctx.author.id)
            else:
                member = member
                userid = str(member.id)

            if col2.count({'userid': userid}) == 0:
                await ctx.send(f"{member.display_name} has not set their profile yet.")

            else:
                results = col2.find({"userid": userid})

                for result in results:
                    note = result['note']
                    follower_ = result["followers"]
                    rep_ = result['reputation']
                    del result['_id']
                    del result['userid']
                    del result['note']
                    del result['followers']
                    del result['reputation']

                em = discord.Embed(description=f"{note}")
                em.set_author(name=f"Viewing {member.display_name}'s profile", icon_url=member.avatar_url)
                em.set_thumbnail(url=member.avatar_url)

                for i in result:
                    value = result[i]
                    em.add_field(name=f"{i.capitalize()}", value=value)
                try:
                    em.set_footer(text = f"Followers: {follower_[0]} ｜ Cookies: {rep_}")
                except:
                    em.set_footer(text=f"Followers: {follower_} ｜ Cookies: {rep_}")

                await ctx.send(embed=em)


    @profile.command(
        usage='<profile set',
        brief="Lets your setup your profile"
    )
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            userid = str(ctx.author.id)

            if col2.count({'userid': userid}) != 0:
                await ctx.send("You have already set up your profile, try <updateprofile if you want to update something")

            else:
                post = {"userid": userid, "followers" : [0], "reputation": 0}
                col2.insert_one(post)

                await ctx.send(f"Ok, let's get your profile set up. I will ask you questions, answer them accordingly. You can abort anytime, just type 'cancel'")

                await asyncio.sleep(2)

                await ctx.send(f"What is your real name/nickname? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col2.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    name = id  # first input
                    myquery = {"userid": userid}
                    newvalues = {"$set": {"Nickname": name}}

                    col2.update_one(myquery, newvalues)

                await ctx.send(f"What is your age? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col2.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    try:
                        age = int(id)  # second input
                        myquery = {"userid": userid}
                        newvalues = {"$set": {"age": age}}

                        col2.update_one(myquery, newvalues)

                    except:
                        await ctx.send(f"Age has to be a number")

                await ctx.send(f"Nationality? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col2.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    nationality = id
                    myquery = {"userid": userid}
                    newvalues = {"$set": {"nationality": nationality}}

                    col2.update_one(myquery, newvalues)

                await ctx.send(f"Birthday? Skip this by typing 'skip'")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                if id.lower() == "skip":
                    pass
                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col2.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return
                else:
                    bday = id
                    myquery = {"userid": userid}
                    newvalues = {"$set": {"Birthday": bday}}

                    col2.update_one(myquery, newvalues)

                await ctx.send(f"Add a description/note to your profile")
                ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
                id = str(ida.content)
                note = id

                if len(note) > 250:
                    await ctx.send(f"Note has to be shorter than 250 characters.")
                    return

                elif id.lower() == "cancel":
                    myquery = { "userid": userid }

                    col2.delete_one(myquery)
                    await ctx.send(f"Profile setup cancelled")
                    return

                myquery = {"userid": userid}
                newvalues = {"$set": {"note": note}}

                col2.update_one(myquery, newvalues)

                await ctx.send(f"Profile Basics Complete, to connect/add a social account, use `<profile connect`")


    @profile.command(
        aliases=['dprofile'],
        usage='<profile delete',
        brief="Permanantly deletes your profile"
    )
    async def delete(self, ctx):
        if ctx.invoked_subcommand is None:

            userid = str(ctx.author.id)

            await ctx.send(f"Are you sure you want to delete your profile? (This action cannot be reversed)")
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=300)
            id = str(ida.content)

            if id.lower() == "yes":
                myquery = { "userid": userid }

                col2.delete_one(myquery)

                await ctx.send(f"You profile was deleted.")
            else:
                await ctx.send(f"Action cancelled")


    @profile.command(
        usage='<profile connect [service] [username] [link (optional)]',
        brief="Lets you connect a service to your profile"
    )
    async def connect(self, ctx, service = None, username = None, link = None):
        if ctx.invoked_subcommand is None:
            userid = str(ctx.author.id)
            results = col2.find({"userid" : userid})
            for result in results:
                del result['_id']
                del result["userid"]
                try:
                    del result["colour"]
                except:
                    pass
                length = len(result)
            if col2.count({"userid" : userid}) != 0:
                try:
                    if length < 12:
                        if service != None and username != None:
                            if link == None:
                                myquery = {"userid": userid}
                                newvalues = {"$set": {service: username}}

                                col2.update_one(myquery, newvalues)
                            else:
                                myquery = {"userid": userid}
                                newvalues = {"$set": {service: f"[{username}]({link})"}}

                                col2.update_one(myquery, newvalues)

                            await ctx.send(f"Added your connection\nYou can add {12 - length} more connections")
                        else:
                            await ctx.send(f"You can add upto {12 - length} more connections")
                            await asyncio.sleep(1)
                            await ctx.send('Write it in as `"<profile connect <service name>" "<username>" <link (optional)>` \nFor example - `Spotify <spotify username> <spotify profile link (optional)>`')
                    else:
                        await ctx.send("You cannot add more connections!")

                except:
                    await ctx.send("HMMM an error occured")

            else:
                await ctx.send("You don't have a profile currently! Try making one by typing `<profile set`")


    @profile.command(
        usage='<xconnect [service]',
        brief="Disconnects a service"
    )
    async def xconnect(self, ctx, *, service = None):
        if ctx.invoked_subcommand is None:
            userid = str(ctx.author.id)
            if service != None:
                service = str(service)

                checks = col2.find({"userid" : userid})
                items = []
                for check in checks:
                    for key in check:
                        items.append(key)

                if service in items:
                    col2.update({'userid': userid}, {"$unset": {f"{service}": 1}}, False, True)
                    await ctx.send("Connection removed")

                else:
                    await ctx.send("I couldn't find that connection, re-check the name")

    @profile.command(
        usage='<follow [member]',
        brief="Lets you follow a member"
    )
    async def follow(self, ctx, member : discord.Member = None):
        if ctx.invoked_subcommand is None:
            if member != None:
                userid = str(member.id)
                if col2.count({"userid" : userid}) != 0:
                    result1 = col2.find({"userid" : userid})
                    for checks in result1:
                        userCheck = checks['followers']

                        try:
                            userCheck = userCheck[1:]
                        except:
                            userCheck = []

                    if ctx.author.id in userCheck:
                        await ctx.send(f"You are already following {member.display_name}")
                    else:
                        await ctx.send(f"Do you want to follow {member.display_name}? (y/n)")
                        answer = await self.client.wait_for('message', check = check(ctx.author), timeout= 20)
                        if str(answer.content) == 'y' or str(answer.content) == 'Y':
                            results = col2.find({"userid" : userid})
                            for result in results:
                                followers = result["followers"]
                            try:
                                followers += 1
                            except:
                                followers[0] += 1
                                followers = followers[0]
                            followers = [followers, ctx.author.id]

                            myquery = {"userid": userid}
                            newvalues = {"$set": {"followers": followers }}

                            col2.update_one(myquery, newvalues)

                            await ctx.send(f"You are now following {member}")
                        else:
                            pass

                else:
                    await ctx.send("The user doesn't have a profile!")

            else:
                await ctx.send("Example usage: `<follow <mention user>`")


    @commands.command(
        aliases = ['rep', 'reputation', 'cookies'],
        usage='<cookie [member]',
        brief="Lets you send members cookies"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, member : discord.Member = None):

        if member == None:
            await ctx.send("You didn't tell me who to give the cookie to")

        else:
            userid = str(member.id)

        if member == ctx.author:
            await ctx.send("Hey, you cannot give yourself cookies")
        else:

            results = col2.find({"userid" : userid})

            repList = []

            for result in results:
                try:
                    rep = result["reputation"]
                except:
                    rep = []

                repList.append(rep)
            try:
                reputation = repList[0]

                reputation += 1

                myquery = {"userid": userid}
                newvalues = {"$set": {"reputation": reputation}}

                col2.update_one(myquery, newvalues)

                await ctx.send(f"**{ctx.author}** gave a cookie to **{member}**")
            except:
                await ctx.send("The mentioned user doesn't have a profile set")



def setup(client):
    client.add_cog(Memory(client))
