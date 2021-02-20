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

        shop = self.shop_items()
        embed = discord.Embed(
            title="Shop:", Description="You can buy anything, \nif you have enough money", color=discord.Colour.random())
        # adding the keys and values
        for i in shop.keys():
            embed.add_field(name=i, value=shop[i], inline=True)
        await ctx.send(embed=embed)

    # TODO: MAKE A SELL COMMAND FOR TMR
    @commands.command()
    async def buy(self, ctx, item='', amount=1): 
        self.account_exist(ctx.author.id)

        shop = self.shop_items()
        if item == '' or item not in shop.keys():
            return await ctx.send(f"Please enter a name of valid item <@{ctx.author.id}>")
        
        cost = float(shop[item][len("Price: "):])*amount
        user_data = self.load_data()
        if cost > user_data[str(ctx.author.id)]["wallet"]:
            return await ctx.send("You don't have enough money in your wallet, consider withdrawing some coins")
        
        user_data[str(ctx.author.id)]["wallet"] -= cost

        # check whether the item is already there
        if item in user_data[str(ctx.author.id)]["inventory"]["items"]:
            index = user_data[str(ctx.author.id)]["inventory"]["items"].index(item)
            user_data[str(ctx.author.id)]["inventory"]["amount"][index] += amount
            user_data[str(ctx.author.id)]["inventory"]["cost"][index] += cost

        else:
            user_data[str(ctx.author.id)]["inventory"]["items"].append(item)
            user_data[str(ctx.author.id)]["inventory"]["amount"].append(amount)
            user_data[str(ctx.author.id)]["inventory"]["cost"].append(cost)

        await ctx.send(f"Successfully bought {amount} {item} for {self.currency} {amount}")
        self.save_data(user_data)

def setup(client):
    client.add_cog(Bussines(client))
