import discord
from discord.ext import commands


class BusinessTransactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buy(self, ctx: discord.Context, item: str, amount=1):
        embed = (
            discord.Embed(
                title=f"Successful {item.capitalize()} purchase",
                description=f"{ctx.author} bought {amount} {item.capitalize()} and paid ⏣ {cost}",
                color=discord.Color.random()
            )
            .add_field(name="", value="", inline=True)
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BusinessTransactions(bot))
