from . import check_user_exists
from discord.ext.commands import Cog, Context, command


class UserCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(alias=["deposit"])
    def dep(self, ctx: Context, amount: int):
        """Allows the user to transfer coins from their wallet to the bank"""
        check_user_exists(user_id=ctx.author.id)

    @command(alias=["with"])
    def withdraw(self, ctx: Context, amount: int):
        """Allows the user to transfer coins from their bank to the wallet"""
        check_user_exists(user_id=ctx.author.id)


def setup(bot):
    bot.add_cog(UserCommands(bot))
