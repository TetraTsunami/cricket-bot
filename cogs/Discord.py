import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import re
import datetime

class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_subcommand(base="discord",
            name="user",
            description="Returns info about a user",
            options=[
                create_option(
                    name="user",
                    description="Name/ID of the user",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="hidden",
                    description="Only shows results to you",
                    option_type=5,
                    required=False
                )
            ])
    async def user_info(self, ctx: SlashContext, user, hidden=False):
        target = await self.bot.fetch_user(re.sub(r'^<@!|>$', '', user))
        embed = discord.Embed(title=f'{target.name}#{target.discriminator}', description=target.mention, color=0xc84268)
        embed.set_thumbnail(url=target. avatar_url)
        embed.add_field(name="ID", value=target.id, inline=False)
        embed.add_field(name="Created", value=formatdate(target.created_at))
        try:
            guild = self.bot.get_guild(ctx.guild_id)
            member = await guild.fetch_member(target.id)
            embed.add_field(name="Joined", value=formatdate(member.joined_at))
        except:
            pass
        finally:
            await ctx.send(embed=embed,hidden=hidden)
            
def formatdate(target: datetime.datetime):
    return target.strftime("%A, %B %d, %Y %I:%M %p")
        
def setup(bot):
    bot.add_cog(Discord(bot))