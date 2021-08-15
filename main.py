from discord.ext import commands
from discord.ext.commands import Context

bot = commands.Bot(command_prefix="%")

@bot.event
async def on_ready():
    print("Ready!!\n")


@bot.command()
async def echo(ctx: Context, *, message):
    """A very simple `echo` command"""
    await ctx.reply(message if message else "Hello")


with open(".env") as file:
    TOKEN = file.readlines()[0].split("=")[1]
bot.run(TOKEN)
