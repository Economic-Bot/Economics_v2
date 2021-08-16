from typing import Optional
from . import USER_DATABASE, check_user_exists, update_database
from discord import Member, Embed, Color
from discord.ext.commands import Cog, Context, command


class UserCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(alias=["deposit"])
    async def dep(self, ctx: Context, amount: int):
        """Allows the user to transfer coins from their wallet to the bank"""
        check_user_exists(user_id=ctx.author.id)
        query = USER_DATABASE.find_one({"_id": "11"})
        bank = query["bank"]
        wallet = query["wallet"]
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
        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        bank = query["bank"]
        wallet = query["wallet"]
        if amount > bank:
            return await ctx.reply("You don't have enough money in your wallet!")

        wallet += amount
        bank -= amount
        update_database(user_id=ctx.author.id, new_data={"wallet": wallet, "bank": bank})
        await ctx.reply(f"You deposited {amount}")

    @command(alias=["balance"])
    async def bal(self, ctx: Context, another_user: Optional[Member] = None):
        """Allows a user to check their balance"""
        if another_user:
            user_id = another_user.id
            user = another_user
        else:
            user_id = ctx.author.id
            user = ctx.author
        check_user_exists(user_id=user_id)

        query = USER_DATABASE.find_one({"_id": user_id})
        bank = query["bank"]
        wallet = query["wallet"]

        title = (
            f"Balance of: {user}"
            f"\nBank: {bank}"
            f"\nWallet: {wallet}"
        )
        embed = Embed(title=title, color=Color.random())
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(UserCommands(bot))
