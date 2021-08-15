from . import USER_DATABASE, check_user_exists, update_database
from discord.ext.commands import Cog, Context, command


class UserCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(alias=["deposit"])
    async def dep(self, ctx: Context, amount: int):
        """Allows the user to transfer coins from their wallet to the bank"""
        check_user_exists(user_id=ctx.author.id)
        query = USER_DATABASE.query({"_id": "11"})

        for i in query:
            bank = i["bank"]
            wallet = i["wallet"]
        if amount > wallet:
            return await ctx.reply("You don't have enough money in your wallet!")

        wallet -= amount
        bank += amount
        update_database(user_id=ctx.author.id, new_data={"wallet": wallet, "bank": bank})
        await ctx.reply(f"You deposited {amount}")

    @command(alias=["with"])
    async def withdraw(self, ctx: Context, amount: int):
        """Allows the user to transfer coins from their bank to the wallet"""
        check_user_exists(user_id=ctx.author.id)
        query = USER_DATABASE.query({"_id": "11"})

        for i in query:
            bank = i["bank"]
            wallet = i["wallet"]
        if amount > bank:
            return await ctx.reply("You don't have enough money in your wallet!")

        wallet += amount
        bank -= amount
        update_database(user_id=ctx.author.id, new_data={"wallet": wallet, "bank": bank})
        await ctx.reply(f"You deposited {amount}")


def setup(bot):
    bot.add_cog(UserCommands(bot))
