# import keep_live   to keep the bot alive
import discord
from discord.ext import commands
import os
import traceback
from API import runner
from multiprocessing import Barrier, Lock, Process

TOKEN = os.environ.get("TOKEN")
IGNORED_FILES = ("__init__.py", "__pycache__")   # ignore this files
client = commands.Bot(command_prefix="%")

# deleting the default `%help`
# client.remove_command('help')


# to see whether the bot is running or not
@client.event
async def on_ready():
    '''shows that the bot is working'''

    print("\n\nIts working !!\n\n")


@client.event
async def on_message(message):
    '''prints out what was typed'''

    author = message.author  # the author
    content = message.content  # the content
    print(f"{author}: {content}")

    if "810963397809537055" in str(content) and str(message.author.id) != "810963397809537055":
        await message.channel.send(f"My prefix: `%{(client, message)}`, send `%{(client, message)}help` to see all the commands <@{author.id}>")

    # to see what command was given
    await client.process_commands(message)


@client.command(aliases=["reload"])
async def re_load_ext(ctx, *name_of_ext):
    """To reload extension(s)"""

    if str(ctx.author.id) == "759129467414380554":
        try:
            for i in name_of_ext:
                client.reload_extension(i)

        except Exception as err:
            await ctx.send(err)

        else:
            await ctx.send(f"{name_of_ext} was successfully reloaded")

    else:
        await ctx.send(f"You don't have perms <@{ctx.author.id}>, _why would you do it though ?_")


@client.command(aliases=["load"])
async def load_ext(ctx, *name_of_ext):
    """To load extension(s)"""

    if str(ctx.author.id) == "759129467414380554":
        try:
            for i in name_of_ext:
                client.load_extension(i)

        except Exception as err:
            await ctx.send(err)

        else:
            await ctx.send(f"{name_of_ext} was successful loaded")

    else:
        await ctx.send(f"You don't have perms <@{ctx.author.id}>, _why would you do it though ?_")


@client.command(aliases=["unload"])
async def unload_ext(ctx, *name_of_ext):
    """To unload extension(s)"""

    if str(ctx.author.id) == "759129467414380554":
        try:
            for i in name_of_ext:
                client.unload_extension(i)

        except Exception as err:
            await ctx.send(err)

        else:
            await ctx.send(f"{name_of_ext} was successful unloaded")

    else:
        await ctx.send(f"You don't have perms <@{ctx.author.id}>, _why would you do it though ?_")


def run_server(*args):
    return runner.start()


def run_bot(*args):
    extensions = [
        f"Cogs.{i[:-3]}"
        for i in os.listdir("./Cogs")
        if i not in IGNORED_FILES
    ]
    for i in extensions:
        try:
            client.load_extension(i)
            print(f"Loaded extension: {i}")
        except Exception:
            print("Failed to load extension: {}".format(i))
            traceback.print_exc()

    return client.run(TOKEN)


if __name__ == '__main__':
    synchronizer = Barrier(2)
    serializer = Lock()
    # Process(target=run_bot, args=(synchronizer, serializer)).start()
    Process(target=run_server, args=(synchronizer, serializer)).start()
