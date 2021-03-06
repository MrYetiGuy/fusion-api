import discord
from make_bot import make_bot
from discord.ext import commands

bot = commands.Bot(command_prefix='reg ')
bot.remove_command('help')

@bot.command(name='help')
async def _help(ctx, *args):
    await ctx.send('```reg add <bot mention> <owner mention>``` Need to replace a current token or change owner? Do ```reg add <bot mention> <owner mention> [current token]``` Admin and need to fix a mistake yourself? Do ```reg add <bot mention> <owner mention> --force```')

@bot.command()
async def add(ctx, bot : discord.Member, owner : discord.Member, current_token=None):
    with open('guilds', 'r') as f:
        if ctx.guild.id not in [int(x) for x in f.read().split('\n') if x]:
            raise Exception('Bot only designed for Fusion Discord Bots guild. Want an API for your own server? Contact me @JellyWX on Fusion Bots guild.')

    if not bot.bot:
        raise Exception('First mention must be a bot')

    elif owner.bot:
        raise Exception('Second mention must not be a bot')

    if current_token in ('--force', '-f') and not ctx.author.guild_permissions.administrator:
        ctx.send('Only admins may override')

    else:
        token, error = make_bot(bot.id, owner.id, current_token, current_token in ('--force', '-f'))

        await ctx.send(embed=discord.Embed(description='''
Token:
```{}```
Notes:
```{}```
'''.format(token, error)))

@add.error
async def add_error(ctx, error):
    await ctx.send(error)
    await ctx.send('```reg add <bot mention> <owner mention>``` Need to replace a current token or change owner? Do ```reg add <bot mention> <owner mention> [current token]``` Admin and need to fix a mistake yourself? Do ```reg add <bot mention> <owner mention> --force```')


with open('token', 'r') as f:
    bot.run(f.read().strip())
