import discord
import requests
from API import utils
from discord.ext import commands
import logging as log

log.basicConfig(
    format='Bot --> %(levelname)s: %(name)s: %(message)s',
    level=log.INFO
)


class BusinessTransactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buy(self, ctx, item: str, amount=1):
        """
        Allows users to buy items from the shop
        :param item: Thing which the user is going to buy
        :param amount: `How many` items the user is going to buy 
        """
        result = requests.get(utils.URL).json()
        cost = result['cost']
        flag = result['flag']

        if flag:
            log.info(
                f"{ctx.author} has enough funds to buy {amount} {item.capitalize()}")
            embed = (
                discord.Embed(
                    title=f"Successful {item.capitalize()} purchase",
                    description=f"{ctx.author} bought {amount} {item.capitalize()} and paid {cost}",
                    color=discord.Color.random()
                )
                .set_footer(text="Thanks for your purchase!", icon_url=ctx.author.avatar_url)
            )
            return await ctx.send(embed=embed)

        if not cost:  # cost == 0.00
            log.info(
                f"{ctx.author} doesn't have enough funds to buy {amount} {item.capitalize()}")
            message = f"You don't have enough money in your wallet to buy {amount} {item.capitalize()}!"
            return await ctx.send(message)


    @commands.command()
    async def sell(self, ctx, item: str, amount=1):
        """
        Allows users to sell items from their inventory
        :param item: Thing which the user is going to sell
        :param amount: `How many` items the user is going to sell 
        """
        result = requests.get(utils.URL).json()
        cost = result['cost']
        flag = result['flag']

        if flag:
            log.info(
                f"{ctx.author} sold {amount} {item.capitalize()} for {cost}")
            
            embed = (
                discord.Embed(
                    title=f"Successful {item.capitalize()} purchase",
                    description=f"{ctx.author} sold {amount} {item.capitalize()} and paid ⏣ {cost}",
                    color=discord.Color.random()
                )
                .set_footer(text="Thanks for your purchase!", icon_url=ctx.author.avatar_url)
            )
            return await ctx.send(embed=embed)

        if not cost:
            log.info(
                f"{ctx.author} doesn't have {amount} {item.capitalize()} to sell for {cost}")
            message = f"You don't have {amount} {item.capitalize()} to sell!"
            return await ctx.send(message)

        log.info(f"{ctx.author} doesn't have enough {item.capitalize()}")
        message = f"You don't have {item.capitalize()} in your inventory!"
        await ctx.send(message)


def setup(bot):
    bot.add_cog(BusinessTransactions(bot))
