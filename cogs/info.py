import discord
from discord.ext import commands


def list_slice(a, limit):
    y = []

    while len(a) > 0:
        y.append(a[:limit])

        a = a[limit:]

    return y


class Info(commands.Cog):
    """Information Commands"""

    def __init__(self, client):
        self.client = client


    @commands.command(
        aliases=['userid'],
        usage='<id [member/none]',
        brief="Returns member's account ID"
    )
    async def id(self, ctx, member: discord.Member=None):

        if not member:
            member=ctx.author

        await ctx.send(embed=discord.Embed(description=f"{member.mention}'s user ID is `{member.id}`"))

    
    @commands.command(
        aliases=['discrim', 'userdiscrim', 'userdiscriminator'],
        usage='<discriminator [member/none]',
        brief="Returns member's account discriminator"
    )
    async def discriminator(self, ctx, member: discord.Member=None):

        if not member:
            member=ctx.author

        await ctx.send(embed=discord.Embed(description=f"{member.mention}'s user discriminator is `#{member.discriminator}`"))


    @commands.command(
        aliases=['emotelist'],
        usage='<emotes',
        brief="Returns all the guild emotes"
    )
    async def emotes(self, ctx):
        guild = ctx.guild

        emo = guild.emojis

        n_animated = 0
        n_normal = 0

        emos = []

        for emote in emo:
            if emote.animated:
                n_animated += 1

                emos.append(f'<a:{emote.name}:{emote.id}>')

            else:
                n_normal += 1

                emos.append(f'<:{emote.name}:{emote.id}>')

        if len(emos) < 25:

            a = ' '.join(emos)

            e = discord.Embed(
                title=f"Emote List — Animated: {n_animated} Regular: {n_normal}",
                description=a
            )

            await ctx.send(embed=e)


        else:
            li = list_slice(emos, 25)

            a = ' '.join(li[0])

            li.pop(0)

            e = discord.Embed(
                title=f"Emote List — Animated: {n_animated} Regular: {n_normal}",
                description=a
            )

            await ctx.send(embed=e)

            for i in range(len(li)):
                e = discord.Embed(
                    description=' '.join(li[i])
                )

                await ctx.send(embed=e)


    @commands.command(
        aliases=['emoji', 'emoteinfo'],
        usage='<emote [custom emote]',
        brief='Returns information for a custom emote'
    )
    async def emote(self, ctx, emo: discord.Emoji=None):

        if not emo:
            return await ctx.send(embed=discord.Embed(description="You need to provide me an emote"))


        e = discord.Embed(
            title="Emote Information",
            description=f"""
Emote Name: {emo.name}
Emote ID: {emo.id}
Animated: {emo.animated}
Guild belonging to: {emo.guild.name} ({emo.guild.id})
Created At: {str(emo.created_at)[:-7]}
[Download]({emo.url})
"""
        )

        e.set_thumbnail(url=emo.url)

        await ctx.reply(embed=e, mention_author=False)

    
    @commands.command(
        usage='<emoteget [emote id]',
        brief='Get an emote by ID'
    )
    async def emoteget(self, ctx, emote: discord.Emoji=None):
        if not emote:
            return await ctx.reply("You didn't give an emote ID", mention_author=False)

        e = discord.Embed(
            title="Emote Information",
            description=f"""
Emote Name: {emote.name}
Emote ID: {emote.id}
Animated: {emote.animated}
Guild belonging to: {emote.guild.name} ({emote.guild.id})
Created At: {str(emote.created_at)[:-7]}
[Download]({emote.url})
"""
        )

        e.set_thumbnail(url=emote.url)

        await ctx.reply(embed=e, mention_author=False)
        


    @commands.command(
        usage='<emotefind [emote name]',
        brief='Makes me find emotes from servers'
    )
    async def emotefind(self, ctx, *, name=None):
        if not name:
            return await ctx.reply("You didn't give an emote name", mention_author=False)

        matches = []

        count = 0

        for guild in self.client.guilds:
            for emote in guild.emojis:
                if name in emote.name:
                    if not len(matches) >= 10:
                        matches.append(emote)
                        count+=1

                    else:
                        break

        if len(matches) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"No matches for emote name '{name}'. Try a different one?"), mention_author=False)

        des = []

        index = 1

        for emote in matches:
            if emote.animated:
                des.append(f"{index}. `{emote.id}` - <a:{emote.name}:{emote.id}>")
                index+=1

            else:
                des.append(f"{index}. `{emote.id}` - <:{emote.name}:{emote.id}>")
                index+=1 
        

        des = '\n'.join(des)

        e = discord.Embed(
            description=des,
            title=f"Emote Search Results for {name}",
        )

        e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        aliases=['guildicon', 'icon'],
        usage='<servericon',
        brief="Shows a preview of the guild's icon"
    )
    async def servericon(self, ctx):
        e = discord.Embed(
            title="Guild Icon"
        )

        e.set_image(url=ctx.guild.icon_url)

        await ctx.reply(embed=e, mention_author=False)

    
    @commands.command(
        aliases=['guildbanner', 'banner'],
        usage='<serverbanner',
        brief="Shows a preview of the guild's banner"
    )
    async def serverbanner(self, ctx):

        if not ctx.guild.banner_url:
            return await ctx.reply("This guild has no banner", mention_author=False)

        e = discord.Embed(
            title="Guild Banner"
        )

        e.set_image(url=ctx.guild.banner_url)

        await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        aliases=['guildsplash', 'splash'],
        usage='<serversplash',
        brief="Shows a preview of the guild's invite splash"
    )
    async def serversplash(self, ctx):

        if not ctx.guild.splash_url:
            return await ctx.reply("This guild has no invite splash", mention_author=False)

        e = discord.Embed(
            title="Guild Splash Banner"
        )

        e.set_image(url=ctx.guild.splash_url)

        await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        aliases=['si'],
        usage='<serverinfo',
        brief="Returns info for a server"
    )
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            title=f"Server Info — {ctx.guild.name}"
        )
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name="Created At", value=f"{str(ctx.guild.created_at)[:-7]}", inline=False)
        embed.add_field(name="Channels",
                        value=f"Voice: {len(ctx.guild.voice_channels)}  Text: {len(ctx.guild.text_channels)}  Category: {len(ctx.guild.categories)}",
                        inline=False)
        embed.add_field(name="Ownership", value=f"{ctx.guild.owner}")
        embed.add_field(name="Tier—Boosts—Boosters",
                        value=f"{ctx.guild.premium_tier}—{ctx.guild.premium_subscription_count}—{len(ctx.guild.premium_subscribers)}",
                        inline=False)
        region = str(ctx.guild.region)
        embed.add_field(name="Server Region", value=f"{region.capitalize()}")
        embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Role Count", value=f"{len(ctx.guild.roles)}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        try:
            embed.set_image(url=f"{ctx.guild.banner_url}")

        except:
            pass

        await ctx.send(embed=embed)


    @commands.command(
        aliases=['ui', 'i', 'me', 'whois'],
        usage='<userinfo [user]',
        brief="Returns info for a user"
    )
    async def userinfo(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        embed = discord.Embed(timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info — {member}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="Member ID", value=member.id)
        embed.add_field(name="Display ID", value=member.display_name)

        created = str(member.created_at)
        joined = str(member.joined_at)

        embed.add_field(name="Created At", value=created[:-7])
        embed.add_field(name="Joined At", value=joined[:-7])

        embed.add_field(name="Top role", value=member.top_role.mention)

        embed.add_field(name="Bot", value=member.bot)

        roles = [role for role in member.roles if role != ctx.guild.default_role]

        if len(roles) == 0:
            embed.add_field(name=f"Roles ({len(roles)})", value="No Roles")
        else:
            embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)

        await ctx.reply(embed=embed, mention_author=False)

    
    @commands.command(
        usage='<roleinfo [role]',
        brief="Returns info for a role"
    )
    async def roleinfo(self, ctx, roles: discord.Role=None):

        if not roles:
            return await ctx.reply("You didn't tell me what role to get info for", mention_author=False)

        em = discord.Embed(
        )
        em.add_field(name="Role ID", value=f"{roles.id}")
        em.add_field(name="Members with", value=f"{len(roles.members)}")
        em.add_field(name="Displayed Sep", value=f"{roles.hoist}")
        em.add_field(name="Created At", value=f"{str(roles.created_at)[:-7]}")
        em.add_field(name="Top Position", value=f"{len(ctx.guild.roles) - roles.position - 1}")
        em.add_field(name="Colour Hex", value=f"{roles.colour}")
        em.set_author(name=f"Role Info — {roles.name}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=em, mention_author=False)


    @commands.command(
        aliases=['channelstats'],
        usage='<channelinfo',
        brief="Returns info for text channel"
    )
    async def channelinfo(self, ctx, channel: discord.TextChannel=None):
        
        if not channel:
            channel = ctx.channel
        
        embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}")
        embed.add_field(name="Channel Guild", value=ctx.guild.name)
        embed.add_field(name="Channel Id", value=channel.id)
        embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}")
        embed.add_field(name="Channel Position", value=channel.position)
        embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay)
        embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw())
        embed.add_field(name="Channel is news?", value=channel.is_news())
        embed.add_field(name="Channel Creation Time", value=channel.created_at)
        embed.add_field(name="Channel Hash", value=hash(channel))

        await ctx.reply(embed=embed, mention_author=False)


    @commands.command(
        aliases=['servermods', 'mods', 'servermoderators', 'serverstaff'],
        usage='<moderators',
        brief="Returns a list of server moderators"
    )
    async def moderators(self, ctx):
        mods = []

        for member in ctx.guild.members:
            if not member.bot:
                if member.guild_permissions.manage_messages:
                    mods.append(member)

        des = ''

        for mod in mods:
            des = des + f'{mod.mention} '

        e = discord.Embed(title="Server Moderators", description=des)

        await ctx.reply(embed=e, mention_author=False)



def setup(client):
    client.add_cog(Info(client))
