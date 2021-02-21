# TODO: MAKE A `INV` COMMAND FOR TMR
from disputils import BotEmbedPaginator
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
        """This is the shop, where `items` can be bought"""

        self.account_exist(ctx.author.id)
        shop = self.shop_items()
        embed = discord.Embed(
            title="Shop:", Description="You can buy anything, \nif you have enough money", color=discord.Colour.random())
        # adding the keys and values
        for i in shop.keys():
            embed.add_field(name=i, value=shop[i], inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item='', amount=1):
        """To allow users to buy `items` from the `shop`"""

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
            index = user_data[str(ctx.author.id)
                              ]["inventory"]["items"].index(item)
            user_data[str(ctx.author.id)
                      ]["inventory"]["amount"][index] += amount
            user_data[str(ctx.author.id)]["inventory"]["cost"][index] += cost

        else:
            user_data[str(ctx.author.id)]["inventory"]["items"].append(item)
            user_data[str(ctx.author.id)]["inventory"]["amount"].append(amount)
            user_data[str(ctx.author.id)]["inventory"]["cost"].append(cost)

        await ctx.send(f"Successfully bought {amount} {item} for {self.currency} {amount}")
        self.save_data(user_data)

    @commands.command()
    async def sell(self, ctx, item='', amount=1):
        """To allow users to sell the items they have previously bought"""

        self.account_exist(ctx.author.id)
        user_data = self.load_data()
        inventory = user_data[str(ctx.author.id)]["inventory"]

        # check whether the item exists or not
        if item not in inventory["items"]:
            return await ctx.send(f"That item doesn't exist in your inventory! <@{ctx.author.id}>")

        # check whethere the amount is bigger than 0
        if amount <= 0:
            return await ctx.send(f"Please enter an amount higher than 0! <@{ctx.author.id}>")

        index = inventory["items"].index(item)
        # check wethere there is enough of the item
        if amount > inventory["amount"][index]:
            return await ctx.send(f"you do not have {amount} {item}! <@{ctx.author.id}>")

        inventory["amount"][index] -= amount
        # cos = cost of sales = cost/amount * amount
        cos = round(
            ((inventory["cost"][index]/inventory["amount"][index]) * amount), 2)

        if inventory["amount"][index] == 0:
            inventory["items"].pop(index)
            inventory["amount"].pop(index)
            inventory["cost"].pop(index)

        await ctx.send(f"You have sold {amount} {item} for {self.currency} {cos}")
        user_data[str(ctx.author.id)]["wallet"] += cos
        self.save_data(user_data)

    def create_embed(self):
        return discord.Embed(title="", description="", color=discord.Colour.random())

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):
        """To allow user to get all the item they have in there inventory"""

        user_data = self.load_data()
        inventory = user_data[str(ctx.author.id)]["inventory"]

        items = inventory["items"]
        cost = inventory["cost"]
        amount = inventory["amount"]

        embed2 = self.create_embed()
        for i in range(len(items)):
            embed2.add_field(name="", value=f"{items[i]} {self.currency} {cost[i]} {amount[i]}", inline=False)

        embeds = [
            discord.Embed(title="Click the arrows to navigate", description="Get all the items you have bought", color=discord.Colour.random()),
            embed2
        ]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


        

def setup(client):
    client.add_cog(Bussines(client))
