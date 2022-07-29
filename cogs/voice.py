import discord
from discord.ext import commands


class Voice(commands.Cog):
    """Voice Commands"""

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await ctx.reply(embed=discord.Embed(description="Unable to find that text/voice channel"), mention_author=False)


    @commands.command(
        aliases=['deafen', 'vcdeafen', 'vcdeaf', 'voicedeaf'],
        usage='<voicedeafen [member]',
        brief='Voice deafen provided member'
    )
    @commands.has_guild_permissions(deafen_members=True)
    async def voicedeafen(self, ctx, member: discord.Member=None):
        if not member:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a member as parameter"), mention_author=False)

        try:
            await member.edit(deafen=True)
            return await ctx.reply(embed=discord.Embed(description=f"Voice deafened {member.mention}. Use `<voiceundeafen` to revert this"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Unable to voice deafen this member"), mention_author=False)


    @commands.command(
        aliases=['deafenall', 'vcdeafenall', 'vcdeafall', 'voicedeafall'],
        usage='<voicedeafenall [voice channel name/id]',
        brief='Voice deafens all users in a voice channel'
    )
    @commands.has_guild_permissions(deafen_members=True)
    async def voicedeafenall(self, ctx, vc: discord.VoiceChannel=None):
        if not vc:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a voice channel as parameter"), mention_author=False)

        if len(vc.members) == 0:
            return await ctx.reply(embed=discord.Embed(description="No members are connected to this voice channel"), mention_author=False)

        try:

            deafened = []

            for member in vc.members:
                try:
                    deafened.append(member.display_name)
                    await member.edit(deafen=True)

                except:
                    pass

            des = '• ' + ', '.join(deafened)
                
            await ctx.reply(embed=discord.Embed(description=f"Voice deafened {len(deafened)} users\n{des}"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="That is not a valid channel, or I do not have sufficient permissions to perform this task"), mention_author=False)


    @commands.command(
        aliases=['undeafenall', 'vcundeafenall', 'vcundeafall', 'voiceundeafall'],
        usage='<voiceundeafenall [voice channel name/id]',
        brief='Voice undeafens all users in a voice channel'
    )
    @commands.has_guild_permissions(deafen_members=True)
    async def voiceundeafenall(self, ctx, vc: discord.VoiceChannel=None):
        if not vc:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a voice channel as parameter"), mention_author=False)

        if len(vc.members) == 0:
            return await ctx.reply(embed=discord.Embed(description="No members are connected to this voice channel"), mention_author=False)

        try:

            undeafened = []

            for member in vc.members:
                try:
                    undeafened.append(member.display_name)
                    await member.edit(deafen=False)

                except:
                    pass

            des = '• ' + ', '.join(undeafened)
                
            await ctx.reply(embed=discord.Embed(description=f"Voice undeafened {len(undeafened)} users\n{des}"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="That is not a valid channel, or I do not have sufficient permissions to perform this task"), mention_author=False)

    
    @commands.command(
        aliases=['undeafen', 'vcundeafen', 'vcundeaf', 'voiceundeaf'],
        usage='<voiceundeafen [member]',
        brief='Voice undeafen provided member'
    )
    @commands.has_guild_permissions(deafen_members=True)
    async def voiceundeafen(self, ctx, member: discord.Member=None):
        if not member:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a member as parameter"), mention_author=False)

        try:
            await member.edit(deafen=False)
            return await ctx.reply(embed=discord.Embed(description=f"Voice undeafened {member.mention}. Use `<voicedeafen` to revert this"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Unable to voice deafen this member"), mention_author=False)


    @commands.command(
        aliases=['vcmute'],
        usage='<voicemute [member]',
        brief='Voice mutes provided member'
    )
    @commands.has_guild_permissions(mute_members=True)
    async def voicemute(self, ctx, member: discord.Member=None):
        if not member:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a member as parameter"), mention_author=False)

        try:
            await member.edit(mute=True)
            return await ctx.reply(embed=discord.Embed(description=f"Voice muted {member.mention}. Use `<voiceunmute` to revert this"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Unable to voice mute this member"), mention_author=False)

    
    @commands.command(
        aliases=['vcunmute'],
        usage='<voiceunmute [member]',
        brief='Voice unmutes provided member'
    )
    @commands.has_guild_permissions(mute_members=True)
    async def voiceunmute(self, ctx, member: discord.Member=None):
        if not member:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a member as parameter"), mention_author=False)

        try:
            await member.edit(mute=False)
            return await ctx.reply(embed=discord.Embed(description=f"Voice unmuted {member.mention}. Use `<voicemute` to revert this"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Unable to voice unmute this member"), mention_author=False)


    @commands.command(
        aliases=['vcmuteall'],
        usage='<voicemuteall [voice channel name/id]',
        brief='Voice mute all users in a voice channel'
    )
    @commands.has_guild_permissions(mute_members=True)
    async def voicemuteall(self, ctx, vc: discord.VoiceChannel=None):
        if not vc:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a voice channel as parameter"), mention_author=False)

        if len(vc.members) == 0:
            return await ctx.reply(embed=discord.Embed(description="No members are connected to this voice channel"), mention_author=False)

        try:

            muted = []

            for member in vc.members:
                try:
                    muted.append(member.display_name)
                    await member.edit(mute=True)

                except:
                    pass

            des = '• ' + ', '.join(muted)
                
            await ctx.reply(embed=discord.Embed(description=f"Voice muted {len(muted)} users\n{des}"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="That is not a valid channel, or I do not have sufficient permissions to perform this task"), mention_author=False)


    @commands.command(
        aliases=['vcunmuteall'],
        usage='<voiceunmuteall [voice channel name/id]',
        brief='Voice unmute all users in a voice channel'
    )
    @commands.has_guild_permissions(mute_members=True)
    async def voiceunmuteall(self, ctx, vc: discord.VoiceChannel=None):
        if not vc:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a voice channel as parameter"), mention_author=False)

        if len(vc.members) == 0:
            return await ctx.reply(embed=discord.Embed(description="No members are connected to this voice channel"), mention_author=False)

        try:

            unmuted = []

            for member in vc.members:
                try:
                    unmuted.append(member.display_name)
                    await member.edit(mute=False)

                except:
                    pass

            des = '• ' + ', '.join(unmuted)
                
            await ctx.reply(embed=discord.Embed(description=f"Voice unmuted {len(unmuted)} users\n{des}"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="That is not a valid channel, or I do not have sufficient permissions to perform this task"), mention_author=False)


    @commands.command(
        aliases=['voiceleave', 'vcdisconnect', 'vcleave', 'vckick'],
        usage='<voicedisconnect [member]',
        brief='Disconnects member from voice channel'
    )
    @commands.has_guild_permissions(move_members=True)
    async def voicedisconnect(self, ctx, member: discord.Member=None):

        if not member:
            return await ctx.reply(embed=discord.Embed(description="You need to provide a member as parameter"), mention_author=False)
        
        if not member.voice.channel:
            return await ctx.reply(embed=discord.Embed(description="Member not connected to voice"), mention_author=False)

        try:
            await member.move_to(None, reason=f'Moved on action by {ctx.author}')
            await ctx.reply(embed=discord.Embed(description=f"Disconnected {member.mention} from voice channel"), mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="Unable to disconnect member from voice. Make sure I have sufficient permissions to perform this task"), mention_author=False)


    @commands.command(
        aliases=['vcleaveall', 'vcdisconnectall', 'voiceleaveall', 'vckickall'],
        usage='<voicedisconnectall [voice channel name/id]',
        brief='Disconnect all users in a voice channel'
    )
    @commands.has_guild_permissions(move_members=True)
    async def voicedisconnectall(self, ctx, vc: discord.VoiceChannel=None):
        if not vc:
            return await ctx.reply(embed=discord.Embed(description="You need provide the voice channel's name/ID that you want me to kick users from"), mention_author=False)

        if len(vc.members) == 0:
            return await ctx.reply(embed=discord.Embed(description="No members are connected to this voice channel"), mention_author=False)

        try:

            moved = []

            for member in vc.members:
                try:
                    await member.move_to(None, reason=f'Moved on action by {ctx.author}')
                    moved.append(member.display_name)
                except:
                    pass

            dis = '• ' + ', '.join(moved)

            e = discord.Embed(
                description=f"Disconnected {len(moved)} users from voice\n{dis}"
            )

            await ctx.reply(embed=e, mention_author=False)

        except:
            return await ctx.reply(embed=discord.Embed(description="That is not a valid channel, or I do not have sufficient permissions to perform this task"), mention_author=False)


    @commands.command(
        aliases=['vcmove'],
        usage='<voicemove [member] [voice channel]',
        brief='Move member to another voice channel'
    )
    async def voicemove(self, ctx, member: discord.Member=None, vc: discord.VoiceChannel=None):

        if not member:
            return await ctx.reply("You didn't tell me who to move", mention_author=False)

        if not vc:
            return await ctx.reply("You didn't tell me what voice channel to move the user to", mention_author=False)

        if not member.voice.channel:
            return await ctx.reply("This member is not connected to voice", mention_author=False)

        try:
            await member.move_to(vc)
            await ctx.reply(embed=discord.Embed(description=f"Moved {member} to {vc.name}"), mention_author=False)

        except:
            return await ctx.reply(embed=discord.Embed(description="That is not a valid channel, or I do not have sufficient permissions to perform this task"), mention_author=False)


    @commands.command(
        aliases=['vcmoveall'],
        usage='<voicemoveall [current voice channel] [new voice channel]',
        brief='Move members to another voice channel'
    )
    async def voicemoveall(self, ctx, vc_i: discord.VoiceChannel=None, vc: discord.VoiceChannel=None):
        if not vc_i:
            return await ctx.reply("You didn't tell me what channel to move members from", mention_author=False)

        if not vc:
            return await ctx.reply("You didn't tell me what channel to move members to", mention_author=False)
        
        if len(vc_i.members) == 0:
            return await ctx.reply("No members are connected to this voice channel", mention_author=False)

        for member in vc_i.members:
            try:
                await member.move_to(vc)
            except:
                pass

        e = discord.Embed(
                description=f"Moved members from {vc_i.name} to {vc.name}"
            )

        await ctx.reply(embed=e, mention_author=False)


    @commands.command(
        aliases=['vcdisconnectglobal'],
        usage=f'<voicedisconnectglobal',
        brief='Disconnect all members connected to voice on the server',
        description='Disconnect all members connected to voice on the server'
    )
    @commands.has_guild_permissions(move_members=True)
    async def voicedisconnectglobal(self, ctx):

        moved = []

        for channel in ctx.guild.voice_channels:
            if len(channel.members) > 0:
                for member in channel.members:
                    await member.move_to(None)
                    moved.append(member.display_name)

        if len(moved) == 0:
            return await ctx.reply('No users connected on voice', mention_author=False)

        dis = '• ' + ', '.join(moved)

        e = discord.Embed(
            description=f"Disconnected {len(moved)} users from voice\n{dis}"
        )

        await ctx.reply(embed=e, mention_author=False)


def setup(client):
    client.add_cog(Voice(client))
