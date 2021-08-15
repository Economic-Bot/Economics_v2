from discord.ext.commands import Bot, Context

bot = Bot(command_prefix="%")

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

