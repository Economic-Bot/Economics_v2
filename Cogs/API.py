import discord
import random
from discord.ext import commands
import aiohttp

class Api(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True, aliases=['memes'])
    async def meme(self, ctx):
        '''fetches a random meme and shows it'''

        if random.randint(0, 1) == 1:
            meme_url = "https://www.reddit.com/r/dankmemes/new.json?sort=top/?t=all"
        else:
            meme_url = "https://www.reddit.com/r/dankmemes/new.json?sort=hot"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(meme_url) as r:
                res = await r.json()
                random_number = random.randint(0, 25)

                try:
                    url = res['data']['children'][random_number]['data']['url']

                # to deal with this particular error
                except IndexError:
                    url = res['data']['children'][1]['data']['url']

                title = res['data']['children'][random_number]['data']['title']

                embed = discord.Embed(
                    title=f"{title}", description=None, color=discord.Color.random())
                embed.set_image(url=url)

                embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)
        

def setup(client):
    client.add_cog(Api(client))
