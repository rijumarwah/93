import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient

uri = 'mongodb+srv://riju:1234@cluster0.fpg3q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

cluster = MongoClient(uri)
db = cluster['in']
col = db['in']


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        

def check_guild(guild_id):

    checks = col.find({str(guild_id): True})

    items = []

    for check in checks:
        for key in check:
            items.append(key)

    if str(guild_id) in items:
        return True

    else:
        return False


def add_guild(guild_id):

    guild_id = str(guild_id)

    post = {guild_id: True, 'count': 0}

    col.insert_one(post)


def get_count(guild_id):

    results = col.find({str(guild_id): True})

    checks = col.find({str(guild_id): True})
    
    items = []

    for check in checks:
        for key in check:
            items.append(key)
    
    if 'count' in items:
        for result in results:
            count = int(result['count']) + 1

            return count


def add_count(guild_id, count):
    q2 = {str(guild_id): True}
    
    v2 = {'$set': { 'count': count }}

    col.update_one(q2, v2)


def add_in(guild_id, user_id, mod_id, count, punishment, reason):
    
    case_id = 'case_' + str(count)

    q = {str(guild_id): True}

    v = {'$set': { str(case_id): { str(user_id): [punishment, reason, mod_id] } }}
    

    col.update_one(q, v)


class Mod(commands.Cog):
    """Moderation Commands"""


    def __init__(self, client):
        self.client = client


    @commands.command(
        usage='<mute [member] [reason]',
        brief="Muted a member"
    )
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member=None, *, reason="Unspecified"):

        if not member:
            return await ctx.reply("You didn't tell me who to mute", mention_author=False)

        if member == ctx.author:
            await ctx.reply("You can't use this on yourself", mention_author=False)
            return

        if member.guild_permissions.manage_messages:
            await ctx.reply("You can't use this on a moderator", mention_author=False)
            return

        try:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not role:
                await ctx.reply(embed=discord.Embed(description="No muted role was found, create one called `Muted` with appropriate permissions"), mention_author=False)
                return

            await member.add_roles(role)

            if not check_guild(ctx.guild.id):
                add_guild(ctx.guild.id)

            case = get_count(ctx.guild.id)

            add_in(ctx.guild.id, member.id, ctx.author.id, case, 'mute', reason)

            add_count(ctx.guild.id, int(case))

            await ctx.reply(embed=discord.Embed(title="Member Muted", description=f"[`[case#{case}]`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `{member}` Reason: {reason}"), mention_author=False)
        except Exception as e:
            print(e)
            await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @commands.command(
        aliases=['xmute'],
        usage='<unmute [member]',
        brief="Unmuted a member"
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member=None, *, reason="Unspecified"):

        if not member:
            return await ctx.reply("You didn't tell me who to unmute", mention_author=False)

        try:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not role:
                await ctx.reply("No muted role was found! Please create one called `Muted`", mention_author=False)
                return

            if role not in member.roles:
                await ctx.reply("This member is not muted.", mention_author=False)
                return

            await member.remove_roles(role)
            await ctx.reply(embed=discord.Embed(title="Member Unmuted", description=f"Unmuted `{member}`"), mention_author=False)
        except:
            await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @commands.command(
        aliases=['delete'],
        usage='<clear [amount]',
        brief="Purges the chat"
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int=50):
        try:
            await ctx.channel.purge(limit=amount + 1)
            a = await ctx.send(embed=discord.Embed(description=f":wastebasket: Purge Complete. Deleted {amount} messages"), mention_author=False)
            await asyncio.sleep(4)
            await a.delete()
        except:
            await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @commands.command(
        aliases=['sm', 'slowmo', 'slow'],
        usage='<slowmode [seconds]',
        brief="Activated a slowmode"
    )
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds=None):

        if not seconds:
            em = discord.Embed(
                description=f"Hey you can use this command like this: `<slowmode 10` or `<slowmode off`\nDuration needs to be 1 second or more and less than 10,000 seconds"
            )

            return await ctx.reply(embed=em, mention_author=False)

        try:
            if seconds == "off":
                await ctx.channel.edit(slowmode_delay=0)
                em = discord.Embed(
                    description=f"Removed slowmode",
                )

                await ctx.reply(embed=em, mention_author=False)
            else:
                seconds_i = int(seconds)
                await ctx.channel.edit(slowmode_delay=seconds_i)
                em = discord.Embed(
                    description=f"Set slowmode to {seconds} seconds",
                )

                await ctx.reply(embed=em, mention_author=False)

        except:
            em = discord.Embed(
                description=f"Usage Example: `<slowmode 10` or `<slowmode off`\nDuration needs to be more than 1 second and lesser than 10,000 seconds",
            )

            await ctx.reply(embed=em, mention_author=False)


    @commands.command(
        usage='<ban [member] [reason]',
        brief="Bans a member from the guild"
    )
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member=None, *, reason="Unspecified"):

        if not member:
            return await ctx.reply("You didn't tell me who to ban", mention_author=False)

        if member.guild_permissions.manage_messages:
            await ctx.reply("You can't use this on a moderator", mention_author=False)
            return

        if not member:
            await ctx.reply("Specify a member to ban", mention_author=False)
            return

        if member == ctx.author:
            await ctx.reply("You cannot ban yourself", mention_author=False)
            return

        try:

            if not check_guild(ctx.guild.id):
                add_guild(ctx.guild.id)

            case = get_count(ctx.guild.id)

            add_in(ctx.guild.id, member.id, ctx.author.id, case, 'ban', reason)

            add_count(ctx.guild.id, int(case))

            embed = discord.Embed(
                title="Member Banned",
                description=f"[`[case#{case}]`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `{member}` was banned\nReason: {reason}",
                )

            await member.ban(reason=reason)

            await ctx.reply(embed=embed, mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Hey it looks like the person you're trying to ban has a role higher than mine. I cannot ban them because of role hierarchy"), mention_author=False)


    @commands.command(
        usage='<kick [member] [reason]',
        brief="Kicks a member from the guild"
    )
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member=None, *, reason="Unspecified"):

        if not member:
            return await ctx.reply("You didn't tell me who to kick", mention_author=False)

        if member.guild_permissions.manage_messages:
            await ctx.reply("You can't use this on a moderator", mention_author=False)
            return

        if not member:
            await ctx.reply("Specify a member to kick", mention_author=False)
            return

        if member == ctx.author:
            await ctx.reply("You cannot kick yourself", mention_author=False)
            return

        try:
            if not check_guild(ctx.guild.id):
                add_guild(ctx.guild.id)

            case = get_count(ctx.guild.id)

            add_in(ctx.guild.id, member.id, ctx.author.id, case, 'kick', reason)

            add_count(ctx.guild.id, int(case))

            embed = discord.Embed(
                title="Member Kicked",
                description=f"[`[case#{case}]`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `{member}` was kicked\n Reason: {reason}",
                )

            await member.kick(reason=reason)
            
            await ctx.reply(embed=embed, mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Hey it looks like the person you're trying to kick has a role higher than mine. I cannot kick them because of role hierarchy"), mention_author=False)
    

    @commands.command(
        aliases=['xban'],
        usage='<unban [id]',
        brief="Unbans a former member"
    )
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, id: int=None):

        if not id:
            return await ctx.reply("You didn't give me a user's ID to unban", mention_author=False)

        try:
            user = await self.client.fetch_user(id)
            await ctx.guild.unban(user)
            embed = discord.Embed(
                description=f"{user.mention} was unbanned",
                )
            return await ctx.reply(embed=embed, mention_author=False)

        except discord.Forbidden:
            embed = discord.Embed(
                description=f"**{ctx.author}** No permission to unban the member",
                )
            return await ctx.reply(embed=embed, mention_author=False)

        except:
            embed = discord.Embed(
                description=f"**{ctx.author}** Error: Banned user not found",
                )
            return await ctx.reply(embed=embed, mention_author=False)


    @commands.command(
        usage='<warn [member] [reason]',
        brief="Warns a member"
    )
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member=None, *, message="Unspecified"):

        if not member:
            return await ctx.reply("You didn't tell me who to warn", mention_author=False)

        if member == ctx.author:
            await ctx.reply("You can't use this on yourself", mention_author=False)
            return

        if member.guild_permissions.manage_messages:
            await ctx.reply("You can't use this on a moderator", mention_author=False)
            return

        if len(message) > 750:
            await ctx.reply(f"Keep the warning under 750 characters", mention_author=False)
            return
        
        em = discord.Embed(description=f"{message}")
        em.set_author(name=f"You were warned on {ctx.guild.name}", icon_url=ctx.guild.icon_url)

        try:
            await member.reply(embed=em)
        except:
            pass

        if not check_guild(ctx.guild.id):
                add_guild(ctx.guild.id)

        case = get_count(ctx.guild.id)

        add_in(ctx.guild.id, member.id, ctx.author.id, case, 'warn', message)

        add_count(ctx.guild.id, int(case))

        em = discord.Embed(title="Member Warned", description=f"[`[case#{case}]`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `{member}` Reason: {message}")

        await ctx.reply(embed=em, mention_author=False)

    
    @commands.command(
        usage='<nick [member] [nick]',
        brief="Set member nickname"
    )
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member=None, *, args):

        if not member:
            return await ctx.reply("You didn't tell me who's nick to change", mention_author=False)

        try:
            await member.edit(nick=args)
            await ctx.reply(f"Changed nickname for {member.mention} to {args}", mention_author=False)
        except:
            await ctx.reply(f"No permissions to change member's nick. Try moving my role over their top role", mention_author=False)
            
            
    @commands.command(
        brief='Creates a guild role with provided name and colour',
        usage='<createrole [name] [colour]'
    )
    @commands.has_guild_permissions(manage_roles=True)
    async def createrole(self, ctx, name=None, col=None):
        if not name:
            return await ctx.reply(embed=discord.Embed(description="You didn't tell me what the role name should be"), mention_author=False)
        
        try:
            if not col:
                r = await ctx.guild.create_role(name=f'{name}')
                await ctx.reply(embed=discord.Embed(description=f"Created role {r.mention}"), mention_author=False)
                
            else:
                col = col.replace('#', ' ')
                col = int(col, 16)
                r = await ctx.guild.create_role(name=f'{name}', colour=col)
                await ctx.reply(embed=discord.Embed(description=f"Created role {r.mention}"), mention_author=False)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"{e}"), mention_author=False)


    @commands.command(
        usage='<nuke [channel]',
        brief="Deletes and clones channel"
    )
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, existing_channel: discord.TextChannel=None):

        if not existing_channel:
            return await ctx.reply("You didn't give me a channel to nuke", mention_author=False)

        try:
            if existing_channel is not None:
                await existing_channel.clone(reason="Has been nuked")
                await existing_channel.delete()
                await ctx.reply(embed=discord.Embed(description=f"Nuked the channel (deleted and re-added)"), mention_author=False)
            else:
                await ctx.reply(f'Could not find this text channel', mention_author=False)
        except:
            await ctx.reply(f"Could not find this text channel / No permissions", mention_author=False)


    @commands.group(
        aliases=['p'],
        usage='<purge [category] [parameter]',
        brief='Purge Utilities'
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title="Purge Commands",
                description="""
`<purge bots [limit]` - Purge messages sent by bots
`<purge user [member] [limit]` - Purge messages from a particular user
`<purge images [limit]` - Purge messages containing images
`<purge attachments [limit]` - Purge messages containing attachments
`<purge embeds [limit]` - Purge messages containing embeds
"""
            )
            await ctx.send(embed=e)


    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def bots(self, ctx, max_messages=50):
        if ctx.invoked_subcommand is None:
            try:
                if max_messages > 5000:
                    await ctx.send("Too many messages (<= 5000)")
                    return
                deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: m.author.bot)
                if len(deleted) == 0:
                    x = await ctx.send(":warning: No messages found by bots within `{0}` searched messages!".format(max_messages))
                else:
                    x = await ctx.send(embed=discord.Embed(description=f":wastebasket: Purge Complete. Deleted {len(deleted)} messages"))
            except:
                await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @purge.command(aliases=['user'])
    @commands.has_permissions(manage_messages=True)
    async def users(self, ctx, member: discord.Member=None, max_messages=50):
        if ctx.invoked_subcommand is None:

            if not member:
                return await ctx.send("No member object provided")

            try:
                if max_messages > 5000:
                    await ctx.send("Too many messages (<= 5000)")
                    return
                deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: m.author == member)
                if len(deleted) == 0:
                    x = await ctx.send(":warning: No messages found by user within `{0}` searched messages!".format(max_messages))
                else:
                    x = await ctx.send(embed=discord.Embed(description=f":wastebasket: Purge Complete. Deleted {len(deleted)} messages"))
            except Exception as e:
                print(e)
                await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def images(self, ctx, max_messages=50):
        if ctx.invoked_subcommand is None:
            try:
                if max_messages > 5000:
                    await ctx.send("Too many messages (<= 5000)")
                    return
                deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: len(m.attachments) or len(m.embeds))
                if len(deleted) == 0:
                    x = await ctx.send(":warning: No messages found containing images within `{0}` searched messages!".format(max_messages))
                else:
                    x = await ctx.send(embed=discord.Embed(description=f":wastebasket: Purge Complete. Deleted {len(deleted)} messages"))
            except:
                await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def attachments(self, ctx, max_messages=50):
        if ctx.invoked_subcommand is None:
            try:
                if max_messages > 5000:
                    await ctx.send("Too many messages (<= 5000)")
                    return
                deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: len(m.attachments))
                if len(deleted) == 0:
                    x = await ctx.send(":warning: No messages found containing attachments within `{0}` searched messages!".format(max_messages))
                else:
                    x = await ctx.send(embed=discord.Embed(description=f":wastebasket: Purge Complete. Deleted {len(deleted)} messages"))
            except:
                await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)


    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def embeds(self, ctx, max_messages=50):
        if ctx.invoked_subcommand is None:
            try:
                if max_messages > 5000:
                    await ctx.send("Too many messages (<= 5000)")
                    return
                deleted = await ctx.channel.purge(limit=max_messages, before=ctx.message, check=lambda m: len(m.embeds))
                if len(deleted) == 0:
                    x = await ctx.send(":warning: No messages found containing embeds within `{0}` searched messages!".format(max_messages))
                else:
                    x = await ctx.send(embed=discord.Embed(description=f":wastebasket: Purge Complete. Deleted {len(deleted)} messages"))
            except:
                await ctx.reply(embed=discord.Embed(description="I wasn't able to do that check my permissions maybe?"), mention_author=False)
    
    @commands.group(
        usage='<invite [category]',
        brief="Invite management"
    )
    async def invites(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(
                description="`<invites list` - Get a list of active instant invites codes\n`<invites delete [code]` - Delete an active invite\n`<invites deleteall` - Delete all active invites\n`<invites info [code]`"
            )

            await ctx.reply(embed=e, mention_author=False)


    @invites.command(
        usage='<invite list',
        brief="Returns a list of active guild invites"
    )
    async def list(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(ctx.guild.invites) == 0:
                return await ctx.reply(embed=discord.Embed(description="There are no active invites on this guild"), mention_author=False)

            inv = []

            for invite in ctx.guild.invites:
                inv.append(f"{invite.code} ({invite.uses})")

            des = ', '.join(inv)

            e = discord.Embed(
                title="Active Guild Invite Codes & Usage",
                description=des
            )

            await ctx.reply(embed=e, mention_author=False)


    @invites.command(
        usage='<invite delete [invite]',
        brief="Revoke an invite"
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def delete(self, ctx, invite: discord.Invite=None):
        if ctx.invoked_subcommand is None:
            if not invite:
                return await ctx.reply(embed=discord.Embed(description="You didn't give me an invite"), mention_author=False)

            try:
                code = invite.code
                await invite.delete()
                await ctx.reply(embed=discord.Embed(description=f"Invite `{code}` was deleted"), mention_author=False)

            except:
                await ctx.reply(embed=discord.Embed(description="Unable to delete invite"), mention_author=False)


    @invites.command(
        usage='<invite deleteall',
        brief="Revokes all active guild invites"
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def deleteall(self, ctx):
        if ctx.invoked_subcommand is None:

            if len(ctx.guild.invites) == 0:
                return await ctx.reply(embed=discord.Embed(description="There are no active invites on this guild"), mention_author=False)

            deleted = []

            for invite in ctx.guild.invites:
                try:
                    deleted.append(invite.code)
                    await invite.delete()
                except:
                    pass

            des = ', '.join(deleted)

            await ctx.reply(embed=discord.Embed(title="Deleted Invites", description=f"{des}\nTotal deleted invites: {len(deleted)}"), mention_author=False)


    @invites.command(
        usage='<invite info [invite]',
        brief="Returns info for an invite"
    )
    async def info(self, ctx, invite: discord.Invite=None):
        if ctx.invoked_subcommand is None:
            if not invite:
                return await ctx.reply(embed=discord.Embed(description="You didn't give me an invite"), mention_author=False)

            e = discord.Embed(title=f"Invite Info for {invite.code}")

            e.add_field(name="Inviter", value=f"{invite.inviter}")
            e.add_field(name="Channel", value=f"{invite.channel}")
            e.add_field(name="Guild", value=f"{invite.guild}")
            e.add_field(name="ID", value=f"{invite.id}")
            e.add_field(name="Max Age", value=f"{invite.max_age}")
            e.add_field(name="Max Uses", value=f"{invite.max_uses}")
            e.add_field(name="Uses", value=f"{invite.uses}")
            e.add_field(name="Created At", value=f"{invite.created_at}")
            e.add_field(name="Revoked", value=f"{invite.revoked}")

            await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        aliases=['lock'],
        usage='<lockdown [channel/none]',
        brief='Locks text channel'
    )
    @commands.has_permissions(manage_guild=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            channel = ctx.channel

        try:

            if ctx.guild.default_role not in channel.overwrites:
                overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                await channel.edit(overwrites=overwrites)
                await ctx.send(embed=discord.Embed(description=f"🔒 {channel.name} has been locked"), mention_author=False)

            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                await ctx.send(embed=discord.Embed(description=f"🔒 {channel.name} has been locked"), mention_author=False)

            else:
                await ctx.send(embed=discord.Embed(description="Text channel already locked. Use `<unlock` to unlock"), mention_author=False)


        except:
            await ctx.send(embed=discord.Embed(description="Could not lock channel. I might not have enough permissions"), mention_author=False)


    @commands.command(
        aliases=['unlock'],
        usage='<lockdown [channel/none]',
        brief='Locks text channel'
    )
    @commands.has_permissions(manage_guild=True)
    async def unlockdown(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            channel = ctx.channel

        try:

            if ctx.guild.default_role not in channel.overwrites:
                await ctx.send(embed=discord.Embed(description="Text channel already unlocked. Use `<lock` to lock"), mention_author=False)

            elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
                await ctx.send(embed=discord.Embed(description="Text channel already unlocked. Use `<lock` to lock"), mention_author=False)

            else:
                overwrites = channel.overwrites[ctx.guild.default_role]
                overwrites.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                await ctx.send(embed=discord.Embed(description=f"🔓 Removed {channel} from lockdown"), mention_author=False)

        except:
            await ctx.send(embed=discord.Embed(description="Could not unlock channel. I might not have enough permissions"), mention_author=False)


    @commands.command(
        usage='<rolename [role] [new name]',
        brief="Edits name for provided role"
    )
    @commands.has_guild_permissions(manage_roles=True)
    async def rolename(self, ctx, role: discord.Role=None, name=None):
        if not role:
            return await ctx.reply(embed=discord.Embed(description="You didn't give me a role parameter"), mention_author=False)

        if not name:
            return await ctx.reply(embed=discord.Embed(description="You didn't tell me what the new role name should be"), mention_author=False)

        try:
            initial = role.name
            await role.edit(name=name)
            await ctx.reply(embed=discord.Embed(description=f"Changed role name from {initial} -> {name}"), mention_author=False)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"An error occured: {e}"), mention_author=False)


    
    @commands.command(
        usage='<rolecolour [role] [new colour]',
        brief="Edits colour for provided role"
    )
    @commands.has_guild_permissions(manage_roles=True)
    async def rolecolour(self, ctx, role: discord.Role=None, colour: str = None):
        if not role:
            return await ctx.reply(embed=discord.Embed(description="You didn't give me a role parameter"), mention_author=False)

        if not colour:
            return await ctx.reply(embed=discord.Embed(description="You didn't tell me what the new role colour should be"), mention_author=False)

        colour = colour.replace('#', '')

        int_val_colour = int(colour, 16)

        try:
            initial = role.colour
            await role.edit(colour=int_val_colour)
            await ctx.reply(embed=discord.Embed(description=f"Changed role colour from {initial} -> #{colour}"), mention_author=False)

        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"An error occured: {e}"), mention_author=False)



    @commands.group(
        aliases=['in', 'infraction'],
        usage='<infractions [category]',
        brief='Infraction system info'
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def infractions(self, ctx):
        if ctx.invoked_subcommand is None:

            e = discord.Embed(description=f"""
`<infractions view [case id]` - View info for a particular case
`<infractions user [member]` - View infractions for a member
`<infractions delete [case id]` - Revoke an active case
""")

            await ctx.reply(embed=e, mention_author=False)


    @infractions.command(
        usage='<infractions view [case id]',
        brief="Returns info a particular case"
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def view(self, ctx, caseid=None):
        if ctx.invoked_subcommand is None:

            if not check_guild(ctx.guild.id):
                return await ctx.reply(embed=discord.Embed(description="There are no registered cases for this guild"), mention_author=False)

            if not caseid:
                return await ctx.reply(embed=discord.Embed(description="You didn't give any case ids"), mention_author=False)

            if not caseid.isdigit():
                return await ctx.reply(embed=discord.Embed(description="Case ids need to be numerical"), mention_author=False)

            case = 'case_' + str(caseid)
            

            checks = col.find({str(ctx.guild.id): True})
            
            items = []

            for check in checks:
                for key in check:
                    items.append(key)


            if not case in items:
                return await ctx.reply(embed=discord.Embed(description="I couldn't find any active cases with that id"), mention_author=False)

            
            results = col.find({str(ctx.guild.id): True})

            for result in results:
                infraction_data = result[case]

            data = infraction_data

            key = next(iter(data))

            user_warned = self.client.get_user(int(key))
            warned_by_user = self.client.get_user(data[key][2])
            punishment = data[key][0]
            reason = data[key][1]

            e = discord.Embed(
                title=f"Infraction Case#{caseid}"
            )

            e.add_field(name="User Warned", value=f"{user_warned}")
            e.add_field(name="Warned by", value=f"{warned_by_user}")
            e.add_field(name="Punishment", value=f"{punishment}")
            e.add_field(name="Reason", value=f"{reason}")

            await ctx.reply(embed=e, mention_author=False)

            
    @infractions.command(
        usage='<infractions user [member]',
        brief='View infractions for a user'
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def user(self, ctx, member: discord.Member=None):
        if ctx.invoked_subcommand is None:

            if not check_guild(ctx.guild.id):
                return await ctx.reply(embed=discord.Embed(description="There are no registered cases for this guild"), mention_author=False)


            if not member:
                return await ctx.reply("You didn't tell me who to check infractions for", mention_author=False)


            member_id = str(member.id)

            checks = col.find({str(ctx.guild.id): True})

            for check in checks:
                data = check


            cases = []


            for i in data:
                if str(i).startswith('case'):
                    if member_id in data[i]:
                        cases.append(f"{str(i).replace('_', '#')} - {data[i][member_id][0]}: {data[i][member_id][1]}")


            if len(cases) == 0:
                return await ctx.send(embed=discord.Embed(description="No active cases for user were found"))


            res = list(chunks(cases, 10))

            pages = []

            count = 1

            for i in res:
                des = '\n'.join(i)

                pages.append(discord.Embed(description=des, title=f"Infractions for {member}").set_footer(text=f"Page {count}/{len(res)}"))

                count += 1


        buttons = ['◀', '▶', '🗑']

        m = await ctx.send(embed=pages[0])


        for reaction in buttons:
            await m.add_reaction(reaction)


        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in buttons

        
        page_track = 0


        while True:

            try:

                reaction, user = await self.client.wait_for('reaction_add', timeout=15, check=check)

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
                    await m.clear_reactions()
                    return

            except asyncio.TimeoutError:
                await m.clear_reactions()
                return

            except Exception as e:
                await ctx.send(e)
                return
            
    
    @infractions.command(
        usage='<infractions delete [case id]',
        aliases=['revoke'],
        brief='Revokes active case'
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def delete(self, ctx, caseid=None):
        if ctx.invoked_subcommand is None:

            if not check_guild(ctx.guild.id):
                return await ctx.reply(embed=discord.Embed(description="There are no registered cases for this guild"), mention_author=False)

            if not caseid:
                return await ctx.reply(embed=discord.Embed(description="You didn't give any case ids"), mention_author=False)

            if not caseid.isdigit():
                return await ctx.reply(embed=discord.Embed(description="Case ids need to be numerical"), mention_author=False)

            
            case = 'case_' + str(caseid)
            

            checks = col.find({str(ctx.guild.id): True})
            
            items = []

            for check in checks:
                for key in check:
                    items.append(key)


            if not case in items:
                return await ctx.reply(embed=discord.Embed(description="I couldn't find any active cases with that id"), mention_author=False)

            
            else:
                col.update_one({str(ctx.guild.id): True}, {"$unset" : {case : 1}}, False, True)
                await ctx.reply(embed=discord.Embed(description=f"Case#{caseid} was revoked"), mention_author=False)



def setup(client):
    client.add_cog(Mod(client))
