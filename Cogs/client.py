import discord
import requests
from API import utils
from discord.ext import commands
import logging as log

log.basicConfig(
    format='Bot --> %(levelname)s: %(name)s: %(message)s',
    level=log.INFO
)


class ClientTransactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["balance"])
    async def bal(self, ctx):
        """
        To allow the user to check their balance
        """
        result = requests.get(utils.URL).json()
        cost = result['cost']

        log.info(f"{ctx.author} checked his/her balance")
        embed = (
            discord.Embed(
                title=f"{ctx.author}'s balance",
                description=f"Wallet: {cost[0]} \nBank: {cost[1]}",
                color=discord.Color.random()
            )
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["with", "wit"])
    async def withdraw(self, ctx, amount: int = 10):
        """
        Allows user to withdraw money from their bank
        :param amount: Amount to be withdrawn 
        """
        result = requests.get(utils.URL).json()
        flag = result['flag']

        if flag:
            log.info(f"{ctx.author} withdrew {amount}")
            return await ctx.send(f"You withdrew {amount}")

        log.info(f"{ctx.author} didn't have enough funds to withdraw {amount}")
        await ctx.send(f"You don't have enough funds to withdraw {amount}!")

    @commands.command(aliases=["deposit"])
    async def dep(self, ctx, amount: int = 10):
        """
        Allows user to deposit money from their wallet
        :param amount: Amount to be deposited
        """
        result = requests.get(utils.URL).json()
        flag = result['flag']

        if flag:
            log.info(f"{ctx.author} deposited {amount}")
            return await ctx.send(f"You deposited {amount}")

        log.info(f"{ctx.author} didn't have enough funds to deposit {amount}")
        await ctx.send(f"You don't have enough funds to deposit {amount}!")



def setup(bot):
    bot.add_cog(ClientTransactions(bot))
