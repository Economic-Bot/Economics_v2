from typing import Optional
from . import USER_DATABASE, check_user_exists, update_database
from discord import Embed, Color
from discord.ext.commands import Cog, Context, command


SHOP = {
    "Laptop": 50, "Mouse": 60, "keyboard": 70,
    "Chair": 80, "Phone": 90, "Monitor": 100
}


class ShopCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def shop(self, ctx: Context):
        """All the user to see all the products available for sell
        """
        embed = Embed(title="Shop", color=Color.random())
        for i in SHOP:
            embed.add_field(name=i, value=str(SHOP[i]))
        await ctx.reply(embed=embed)

    @command()
    async def buy(self, ctx: Context, amount: Optional[int] = 1, product: Optional[str] = None):
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

        if product.capitalize() not in SHOP:
            return await ctx.reply(f"{product!r} isn't present in the shop")

        query = USER_DATABASE.find_one({"_id": ctx.author.id})
        wallet = query["wallet"]
        total_cost = SHOP[product] * amount

        if total_cost > wallet:
            # user doesn't have enough funds
            return await ctx.reply(
                f"You don't have enough money in your wallet to buy {amount} {product}"
            )
        wallet -= total_cost
        update_database(user_id=ctx.author.id, new_data={"wallet": wallet})
        await ctx.reply(f"You successfully bought {amount} {product} for {total_cost}")


def setup(bot):
    bot.add_cog(ShopCommands(bot))
