import os
import re

import discord
import requests
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

from .utils.embed import simple_embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    discord_utils = SlashCommandGroup("discord", "Commands related to Discord.")
    
    @discord_utils.command(description="Returns info about a user")
    async def user(
        self,
        ctx,
        target: Option(str, 'The user you would like to harass') = 0, 
        hidden: Option(bool, 'Show results in an ephemeral message', required=False) = False
                   ):
        user = self.bot.get_user(re.sub('^<@|!|>$', '', target))
        if user == None:
            user = await self.bot.fetch_user(re.sub('^<@|!|>$', '', target))
        embed = discord.Embed(title=f'{user.name}#{user.discriminator}', description=user.mention, color=0xc84268)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Created", value=discord.utils.format_dt(user.created_at))
        try:
            embed.add_field(name="Joined", value=discord.utils.format_dt(user.joined_at))
        except:
            pass
        await ctx.respond(embed=embed,ephemeral=hidden)
    
    @discord_utils.command(description="Returns info about a custom emoji")
    async def emote(self, ctx, emoji: Option(str, 'The emoji you\'d like to download')):
        if not re.search('^<.?:.*:.*>$', emoji):
            return await ctx.respond(embed=simple_embed('Emoji', 'Failure','That\'s not a custom emoji??'),ephemeral=True)
        id = re.sub(r'^<.?:.*:|>$', '', emoji)
        name = re.sub(r'^<.?:|:.*>$', '', emoji)
        animated = False
        if re.search(r'^<a:', emoji):
            animated = True
        embed = discord.Embed(title="Emoji", color=0xc84268)
        embed.set_image(url=url(id, animated=animated))
        embed.add_field(name="Name", value=f"`{name}`")
        embed.add_field(name="Animated", value=animated)
        embed.add_field(name="ID", value=f"`{id}`")
        embed.add_field(name="URL", value=url(id, animated=animated), inline=False)
        await ctx.respond(embed=embed)
            
# def formatdate(target: datetime.datetime):
#     target = target.replace(tzinfo=datetime.timezone.utc)
#     target_cst = target.astimezone(datetime.timezone(datetime.timedelta(hours=-6)))
#     return target_cst.strftime("%A, %B %d, %Y %I:%M %p CST")

def url(id, *, animated: bool = False):
	# Convert an emote ID to the image URL for that emote.
	extension = 'gif' if animated else 'png'
	return f'https://cdn.discordapp.com/emojis/{id}.{extension}'

def setup(bot):
    bot.add_cog(Discord(bot))
