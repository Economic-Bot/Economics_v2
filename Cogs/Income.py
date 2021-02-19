import discord
import json
from utils import Main_checks
from discord.ext import commands
import random


class Income(Main_checks.MainChecks, commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def beg(self, ctx):
        """To allow user to get free money"""

        self.account_exist(ctx.author.id)
        user_data = self.load_data()

        if not random.randint(0, 10) in (6, 9):
            money_received = random.randint(
                0, user_data[str(ctx.author.id)]["wallet"])  # get a random number
            user_data[str(ctx.author.id)]["wallet"] += money_received

            self.save_data(user_data)  # save the new info
            return await ctx.send(f"You have receive `{self.currency} {money_received}` _from a stranger_ <@{ctx.author.id}>")

        # the requester didn't get anything
        return await ctx.send(f"You didn't receive anything! <@{ctx.author.id}>")


class Bussines(Income):
    @commands.command()
    async def shop(self, ctx):
        self.account_exist(ctx.author.id)

        shop = self.shop_items(ctx)
        embed = discord.Embed(
            title="Shop:", Description="You can buy anything, \nif you have enough money", color=discord.Colour.random())
        # adding the keys and values
        for i in shop.keys():
            embed.add_field(name=i, value=shop[i], inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Bussines(client))
