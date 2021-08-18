from typing import Dict, Optional
from . import USER_DATABASE, SHOP, check_user_exists, update_database
from discord import Embed, Color, Member
from discord.ext.commands import Cog, Context, command


class ShopCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def shop(self, ctx: Context):
        """All the user to see all the products available for sell
        """
        embed = Embed(title="Shop", color=Color.random())
        for i in SHOP:
            embed.add_field(name=i.capitalize(), value=str(SHOP[i]))
        await ctx.reply(embed=embed)

    @command()
    async def sell(self, ctx: Context, amount: int, item: Optional[str] = "None"):
        """Allows the user to sell items from their inventory"""
        check_user_exists(user_id=ctx.author.id)

        if not isinstance(amount, int):
            item = amount
            amount = 1

        if not isinstance(amount, int):
            return await ctx.reply(f"{amount!r} isn't a valid amount")

        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        wallet = query["wallet"]
        inventory: Dict[str, int] = query["inventory"]

        if item.lower() not in inventory:
            return await ctx.reply(f"You don't own {item!r}")

        if inventory[item] < amount:
            return await ctx.reply(f"You don't own {amount} {item}!")

        cost = SHOP[item.lower()] * amount
        wallet += cost
        inventory[item] -= amount

        if inventory[item] <= 0:
            del inventory[item]

        new_data = {"wallet": wallet, "inventory": inventory}
        update_database(user_id=ctx.author.id, new_data=new_data)
        await ctx.reply(f"You sold {amount} {item} for {cost}")

    @command()
    async def buy(self, ctx: Context, amount: Optional[int] = 1, product: Optional[str] = "None"):
        """Allows the user to buy a specific product

        Args:
            amount (Optional[int], optional): Quantity of the product. Defaults to 1.
            product (Optional[str], optional): Name of the product. Defaults to None.
        """
        check_user_exists(user_id=ctx.author.id)

        if not isinstance(amount, int) and not product:
            # user did something like: `%buy laptop` etc
            product = amount
            amount = 1

        elif not isinstance(amount, int):
            return await ctx.reply(f"{amount!r} isn't a valid amount")

        elif amount <= 0:
            amount = 1

        if product.lower() not in SHOP:
            return await ctx.reply(f"{product!r} isn't present in the shop")

        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        wallet = query["wallet"]
        inventory: Dict[str, int] = query["inventory"]
        total_cost = SHOP[product.lower()] * amount

        if total_cost > wallet:
            # user doesn't have enough funds
            return await ctx.reply(
                f"You don't have enough money in your wallet to buy {amount} {product}"
            )
        wallet -= total_cost
        if product in inventory:
            inventory[product.lower()] = inventory[product.lower()] + amount
        else:
            inventory[product.lower()] = amount
        new_data = {
            "wallet": wallet,
            "inventory": inventory
        }

        update_database(user_id=ctx.author.id, new_data=new_data)
        await ctx.reply(f"You successfully bought {amount} {product.lower()} for {total_cost}")

    @command(aliases=["inv"])
    async def inventory(self, ctx: Context, another_user: Optional[Member] = None):
        """Allows the user to check their (or another user's) inventory
        """
        if another_user:
            user_id = another_user.id
            user = another_user
        else:
            user_id = ctx.author.id
            user = ctx.author
        check_user_exists(user_id=user_id)
        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        embed = Embed(title=f"{user}'s inventory", color=Color.random())
        inventory = query["inventory"]
        for i in inventory:
            embed.add_field(
                name=f"{i}",
                value=f"Amount: {inventory[i]}\nWorth: {SHOP[i] * inventory[i]}"
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ShopCommands(bot))
