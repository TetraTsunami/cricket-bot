from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission
from discord_slash.model import SlashCommandPermissionType


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_slash(name="say",
                description="Make me say something like the grim puppetmaster you wish you could be.", options=[
                create_option(
                    name="text",
                    description="What you'd like to say",
                    option_type=3,
                    required=True
                )
            ])
    @cog_ext.permission(guild_id=534780027502460950,
                permissions=[
                    create_permission(534780027502460950, SlashCommandPermissionType.ROLE, False),
                    create_permission(541084193296482314, SlashCommandPermissionType.ROLE, True)
                ]
            )
    async def bot_say(self, ctx: SlashContext, text):
        await ctx.channel.send(content=text)
        await ctx.send("<:photothumbsup:886416067021381663><:Yeah:870075068644999248>",hidden=True)
        

def setup(bot):
    bot.add_cog(Bot(bot))