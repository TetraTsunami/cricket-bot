from cogs.utils.embed import command_embed
from discord.commands import slash_command
from discord.ext import commands


class MetaCog(commands.Cog, name="help command"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description="Returns info about the bot's ping")
    async def ping(self, ctx):
        await ctx.respond(embed=command_embed(f"⚡ {round(self.bot.latency * 1000)} ms"))

    # @slash_command(description="Display the help message.")
    # @commands.cooldown(1, 2, commands.BucketType.member)
    # async def help(self, ctx, command: str = None):

    #     commandName2 = None
    #     stop = False

    #     if command is not None:
    #         for i in self.bot.commands:
    #             if i.name == command.lower():
    #                 commandName2 = i
    #                 break
    #             else:
    #                 for j in i.aliases:
    #                     if j == command.lower():
    #                         commandName2 = i
    #                         stop = True
    #                         break
    #                     if stop is True:
    #                         break

    #         if commandName2 is None:
    #             await ctx.channel.send("No command found!")
    #         else:
    #             embed = discord.Embed(
    #                 title=f"{commandName2.name.upper()} Command",
    #                 description="",
    #                 color=randint(0, 0xFFFFFF),
    #             )
    #             embed.set_thumbnail(url=f"{self.bot.user.avatar}")
    #             embed.add_field(
    #                 name=f"Name", value=f"{commandName2.name}", inline=False
    #             )
    #             aliases = commandName2.aliases
    #             aliasList = ""
    #             if len(aliases) > 0:
    #                 for alias in aliases:
    #                     aliasList += alias + ", "
    #                 aliasList = aliasList[:-2]
    #                 embed.add_field(name=f"Aliases", value=aliasList)
    #             else:
    #                 embed.add_field(name=f"Aliases", value="None", inline=False)

    #             if commandName2.usage is None:
    #                 embed.add_field(name=f"Usage", value=f"None", inline=False)
    #             else:
    #                 embed.add_field(
    #                     name=f"Usage",
    #                     value=f"{self.bot.command_prefix}{commandName2.name} {commandName2.usage}",
    #                     inline=False,
    #                 )
    #             embed.add_field(
    #                 name=f"Description",
    #                 value=f"{commandName2.description}",
    #                 inline=False,
    #             )
    #             await ctx.channel.send(embed=embed)
    #     else:
    #         embed = discord.Embed(
    #             title=f"Help page",
    #             description=f"{self.bot.command_prefix}help (commandName), display the help list or the help data for a specific command.",
    #             color=randint(0, 0xFFFFFF),
    #         )
    #         embed.set_thumbnail(url=f"{self.bot.user.avatar}")
    #         for i in self.bot.commands:
    #             embed.add_field(name=i.name, value=i.description, inline=False)
    #         await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    # bot.remove_command("help")
    bot.add_cog(MetaCog(bot))
