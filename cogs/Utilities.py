from discord.ext import commands
from discord.commands import slash_command, permissions, Option


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(description="Make me say something like the grim puppetmaster you wish you could be.", default_permission=False) 
    # options=[
    #             create_option(
    #                 name="text",
    #                 description="What you'd like to say",
    #                 option_type=3,
    #                 required=True
    #             )
    #         ])
    @permissions.has_role("Mod Squad")
    async def say(self, ctx, text: Option(str, 'What you\'d like to say')):
        await ctx.channel.send(content=text)
        await ctx.respond("<:photothumbsup:886416067021381663><:Yeah:870075068644999248>",ephemeral=True)
        

def setup(bot):
    bot.add_cog(Utilities(bot))