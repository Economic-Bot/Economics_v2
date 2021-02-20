import discord
from discord.ext import commands
import traceback
red_cross = "❌"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.reply(f"```{error}```")

        if isinstance(error, commands.CommandNotFound): 
            print(f"Commands {error} isn't found")
        
        if isinstance(error, commands.MissingRequiredArgument):
            params = [ctx.command.clean_params[i]
                      for i in ctx.command.clean_params]
            y = ['```{}{} '.format("$", ctx.command.name), '```']

            for i in params:
                y.insert(-1, '<' + i.name + '> ')
            y.insert(-1, '\n\n' + error.args[0])
            return await ctx.message.reply(''.join(y))

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.message.reply(embed=discord.Embed(
                description='You need **{}** perms to complete this actions.'.format(
                    ' '.join(error.missing_perms[0].split('_'))),
                colour=discord.Colour.red()
            ))

        elif isinstance(error, commands.BotMissingPermissions):
            if error.missing_perms[0] == 'send_messages':
                return

            return await ctx.message.reply(
                embed=discord.Embed(
                    description='<:Red_Cross:810183128324374598> I am missing **{}** permissions.'.format(
                        ' '.join(error.missing_perms[0].split('_'))),
                    colour=discord.Colour.red()
                ))

        elif isinstance(error, discord.ext.commands.DisabledCommand):

            return await ctx.message.reply(embed=discord.Embed(
                description='<:Red_Cross:810183128324374598> This command has been disabled. Re-enable it use it again!',
                colour=discord.Colour.red()
            ))

        elif isinstance(error, (commands.errors.MemberNotFound, commands.errors.UserNotFound)):
            return await ctx.message.reply(embed=discord.Embed(
                description="<:Red_Cross:810183128324374598> Member named **{}** was not found!".format(
                    error.argument),
                colour=discord.Colour.red()
            ))

        elif isinstance(error, commands.errors.ChannelNotFound):
            return await ctx.message.reply(embed=discord.Embed(
                description='<:Red_Cross:810183128324374598> Channel named **{}** cannot be found! Retry with a valid channel.'.format(
                    error.argument),
                colour=discord.Colour.red()
            ))

        elif isinstance(error, commands.errors.RoleNotFound):
            return await ctx.message.reply(embed=discord.Embed(
                description='<:Red_Cross:810183128324374598> Role named **{}** cannot be found!'.format(
                    error.argument),
                colour=discord.Colour.red()
            ))

        else:
            channel = self.bot.get_channel(812426694513131531)
            # await channel.send(f'```{error}```')
            error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
            await channel.send('**Error in the command {}**\n```\n'.format(ctx.command.name) + ''.join(map(str, error)) + '\n```')
            # await ctx.message.reply(f"```{error}```")

def setup(bot):
    bot.add_cog(Events(bot))
