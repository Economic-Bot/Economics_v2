from random import randint
from . import USER_DATABASE, check_user_exists, update_database
from discord import Member
from discord.ext.commands import Cog, Context, command


class RevenueCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

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
            wallet += luck/100 * other_user_query["wallet"]
            # the other user lost money
            await ctx.reply(f"You got {luck/100 * other_user_query['wallet']}")
            other_user_query["wallet"] *= (100-luck)/100

        update_database(user_id=ctx.author.id, new_data={"wallet": wallet})
        update_database(user_id=other_user.id, new_data={"wallet": other_user_query["wallet"]})


def setup(bot):
    bot.add_cog(RevenueCommands(bot))
