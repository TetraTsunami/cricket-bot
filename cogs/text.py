import owo
from discord.commands import Option, SlashCommandGroup, slash_command
from discord.ext import commands

from .utils.embed import command_embed

deleted_messages = {}
edited_messages = {"before": {}, "after": {}}


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Owoify your text!")
    async def owoify(self, ctx, text: Option(str, "What you'd like to say")):
        owotext = owo.owo(text)
        await ctx.respond(
            embed=command_embed(ctx, "Owoify", "", owotext), ephemeral=True
        )


def setup(bot):
    bot.add_cog(Utilities(bot))
