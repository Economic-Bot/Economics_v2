from os import listdir
from discord.ext.commands import Bot, Context

bot = Bot(command_prefix="%")


@bot.event
async def on_ready():
    print("\n\nReady!!\n")


@bot.command()
async def echo(ctx: Context, *, message):
    """A very simple `echo` command"""
    await ctx.reply(message if message else "Hello")


@bot.command()
async def reload(ctx: Context, extension: str):
    if ctx.author.id != 759129467414380554:
        return await ctx.reply("What are you on?")

    try:
        bot.reload_extension(f"Commands.{extension}")
        await ctx.send(f"Reloaded: {extension}")
    except Exception as error:
        await ctx.send(f"Couldn't load: {i!r}")
        await ctx.send(f"Error: {extension}")
        print(f"Couldn't load: {i!r}")
        print(f"Error: {error!r}")


with open(".env") as file:
    TOKEN = file.readlines()[0].split("=")[1]

file_to_ignore = ("__init__.py",)
commands = [
    f"Commands.{i[:-3]}"
    for i in listdir("Commands/")
    if i[-3:] == ".py" and i not in file_to_ignore
]
for i in commands:
    try:
        bot.load_extension(i)
        print(f"Loaded: {i!r}")
    except Exception as error:
        print(f"Couldn't load: {i!r}")
        print(f"Error: {error!r}")

bot.run(TOKEN)
