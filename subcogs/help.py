
import discord
from discord.ext import commands
import os


def cog_list():
    coglist = []
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            name = filename.replace('.py', '')
            coglist.append(name)
    
    return coglist


def generate_module_list():
    cogs = cog_list()

    cog_cap = []

    for i in cogs:
        cog_cap.append(i.capitalize())
        
    cog_cap = sorted(cog_cap)

    des = "• " + "\n• ".join(cog_cap)

    return des


class Help(commands.Cog):
    """Help Commands"""

    def __init__(self, client):
        self.client = client


    @commands.command(
        usage="<help [module]",
        brief="Returns a help page",
    )
    async def help(self, ctx, sub=None):

        if not sub:

            about = {
                'animanga': 'Anime and manga',
                'basic': 'Basic and bot',
                'fun': 'Fun commands',
                'info': 'Informative commands',
                'memory': 'Memory related',
                'misc': 'Miscellaneous',
                'mod': 'Server administration',
                'search': 'Search related',
                'settings' : 'Server settings', 
                'utility': 'Utility commands',
                'voice': 'Voice moderation'
            }

            des = generate_module_list()

            e = discord.Embed(
                title='Categories',
                description=f'Use `<help [command]` for more info on a command\nAlso `<help [category]` for more info on a category\nFor more help, join the support server [https://discord.gg/FGY7pmZFk2](https://discord.gg/FGY7pmZFk2)\n{des}'
            )

            return await ctx.reply(embed=e, mention_author=False)

        sub = sub.lower()

        cogs = cog_list()

        if sub in cogs:

            try:

                c = self.client.get_cog(str(sub).capitalize())

                commands = c.get_commands()

                cms = []

                for i in commands:
                    cms.append(f'`{i.name}`')
                
                desc = f'  '.join(cms)

                desc = desc + '\n\n' + 'Try `<help [command]` for more info on a command'
                
                e = discord.Embed(title=f'{sub.capitalize()} Category', description=desc)

                return await ctx.reply(embed=e, mention_author=False)

            except Exception as e:
                await ctx.send(e)

        else:
            command = sub.lower()

            cmd = self.client.get_command(command)

            if not cmd:
                return await ctx.reply(embed=discord.Embed(description="That is not a valid command name"), mention_author=False)

            if len(cmd.aliases) == 0:
                aliases = "No Aliases"
            
            else:
                aliases = ', '.join(cmd.aliases)

            des = f'Description: {cmd.brief}\n\n**Aliases**\n`{aliases}`\n**Usage**\n`{cmd.usage}`'

            e = discord.Embed(
                title=f"Command", description=des
            )

            await ctx.reply(embed=e, mention_author=False)


def setup(client):
    client.add_cog(Help(client))
