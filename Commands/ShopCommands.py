from discord import Embed, Color
from discord.ext.commands import Cog, Context, command


class ShopCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def shop(self, ctx: Context):
        embed = (
            Embed(title="Shop", color=Color.random())
            .add_field(name="Laptop", value="50", inline=True)
            .add_field(name="Mouse", value="60", inline=True)
            .add_field(name="keyboard", value="70", inline=True)

            .add_field(name="Chair", value="80", inline=True)
            .add_field(name="Phone", value="90", inline=True)
            .add_field(name="Mouse", value="100", inline=True)
        )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(ShopCommands(bot))
