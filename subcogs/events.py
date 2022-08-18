import discord
from discord.ext import commands
import time


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=discord.Embed(description="You didn't pass in all parameters. Confused? Try `<command [command]`"), mention_author=False)
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the `{}` permission to use this command.'.format(fmt)
            await ctx.reply(embed=discord.Embed(description=f"{_message}"), mention_author=False)
            return

        if isinstance(error, commands.CommandOnCooldown):
            coold = str(time.strftime('%H:%M:%S', time.gmtime(error.retry_after)))
            await ctx.reply(embed=discord.Embed(description=f"This command is on cooldown `{coold}`"), mention_author=False)
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the `{}` permission to run this command.'.format(fmt)
            await ctx.reply(embed=discord.Embed(description=f"{_message}"), mention_author=False)
            return

        
def setup(client):
    client.add_cog(Events(client))
