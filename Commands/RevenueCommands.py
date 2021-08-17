from random import randint
from . import USER_DATABASE, check_user_exists, update_database
from discord import Member
from discord.ext.commands import Cog, Context, command


class RevenueCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def beg(self, ctx: Context):
        """Allows the user to get free coins if they are lucky enough"""
        check_user_exists(user_id=ctx.author.id)
        luck = randint(1, 13)
        if luck in [1, 9, 6]:
            # the user had bad luck, rip
            return await ctx.reply("None gave you a single cent :/")

        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        query["wallet"] += luck * 100
        update_database(user_id=ctx.author.id, new_data={"wallet": query["wallet"]})
        await ctx.reply(f"Somone gave you {luck*100}")

    @command()
    async def rob(self, ctx: Context, other_user: Member):
        """Allows a user to rob another user to gain more money"""
        check_user_exists(user_id=ctx.author.id)
        check_user_exists(user_id=other_user.id)

        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        other_user_query = USER_DATABASE.find_one({"_id": other_user.id})
        wallet = query["wallet"]
        luck = randint(1, 13)
        if luck in [1, 9, 6]:
            # the user had bad luck, rip
            wallet -= 100
            await ctx.send(f"You got caught, and had to pay 100 to <@{other_user.id}>")
        else:
            # the sender received money
            wallet += int(luck/100 * other_user_query["wallet"])
            # the other user lost money
            await ctx.reply(f"You got {int(luck/100 * other_user_query['wallet'])}")
            other_user_query["wallet"] *= int((100-luck)/100)

        update_database(user_id=ctx.author.id, new_data={"wallet": wallet})
        update_database(user_id=other_user.id, new_data={"wallet": other_user_query["wallet"]})

    @command(aliases=["send"])
    async def give(self, ctx: Context, amount: int, other_user: Member):
        """Allows the user to give/send money to each other"""
        check_user_exists(user_id=ctx.author.id)
        check_user_exists(user_id=other_user.id)

        wallet = USER_DATABASE.find_one({"_id": ctx.author.id})["wallet"]
        other_user_wallet = USER_DATABASE.find_one({"_id": other_user.id})["wallet"]

        if wallet < amount:
            return await ctx.reply(f"You don't have {wallet!r} in your wallet!")

        wallet -= amount
        other_user_wallet += amount
        update_database(user_id=ctx.author.id, new_data={"wallet": wallet})
        update_database(user_id=other_user.id, new_data={"wallet": other_user_wallet})
        await ctx.reply(f"You send {amount} to <@{other_user.id}>")

    @command(aliases=["gamble"])
    async def bet(ctx: Context, amount: int):
        """Allows the user to gamble and gain (or loose) money"""
        check_user_exists(user_id=ctx.author.id)
        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        luck = randint(1, 13)
        if luck in [1, 9, 6]:
            # the user had bad luck, rip
            query["wallet"] -= amount
            update_database(user_id=ctx.author.id, new_data={"wallet": query["wallet"]})
            return await ctx.reply(f"You lost {amount}!")

        query["wallet"] += amount
        update_database(user_id=ctx.author.id, new_data={"wallet": query["wallet"]})
        await ctx.reply(f"You won {amount}!")


def setup(bot):
    bot.add_cog(RevenueCommands(bot))
