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
    
    @discord_utils.command(description="Returns info about a user (or yourself!)")
    async def user(
        self,
        ctx,
        user: Option(discord.Member, 'Who you would like to harass (or nobody at all)') = 0, 
        hidden: Option(bool, 'Show results in an ephemeral message') = False
                   ):
        if user == 0:
            user = ctx.author
            user = await self.bot.fetch_user(re.sub(r'^<@|!|>$', '', user))
        embed = discord.Embed(title=f'{user.name}#{user.discriminator}', description=user.mention, color=0xc84268)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Created", value=discord.utils.format_dt(user.created_at))
        try:
            embed.add_field(name="Joined", value=discord.utils.format_dt(user.joined_at))
        except:
            pass
        await ctx.respond(embed=embed,ephemeral=hidden)
    
    
    @discord_utils.command(description="Starts an activity in your current voice channel")
    async def activity(
        self,
        ctx,
        activity: Option(str, 'Activity (defaults to YouTube)', choices=['Betrayal.io', 'Chess In The Park', 'YouTube Together']) = 'YouTube Together', 
        hidden: Option(bool, 'Show results in an ephemeral message') = False
                   ):
        ACTIVITY_IDS = {
            'Betrayal.io':773336526917861400, 
            'Chess In The Park':832012774040141894,
            'YouTube Together':755600276941176913
        }
        activity_id = ACTIVITY_IDS[activity]
        if not ctx.author.voice.channel:
            return await ctx.respond('get in a voice channel, then we can talk', hidden=True)
        try:
            target = ctx.author.voice.channel
            r = requests.post(f"https://discord.com/api/v8/channels/{target.id}/invites", json = {
                    "max_age": 600,
                    "max_uses": 2,
                    "target_application_id": activity_id,
                    "target_type": 2,
                    "temporary": False}, headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"})
            invite = r.json()
            if r.status_code != 200:
                if activity_id == "755600276941176913": 
                    embed=simple_embed('YouTube Activity', 'YouTube','Permissions')
                else:
                    embed=simple_embed('Discord Activity', 'Discord','Permissions')
                return await ctx.respond(embed=embed,ephemeral=True)
            if activity == "755600276941176913": 
                embed=simple_embed('YouTube Activity', 'YouTube', f"[Start a YouTube session in {ctx.author.voice.channel}](https://discord.gg/{r.json()['code']})")
            else:
                embed=simple_embed('Discord Activity', 'Discord',f"[Start an Activity session in {ctx.author.voice.channel}](https://discord.gg/{r.json()['code']})")
            await ctx.respond(embed=embed,ephemeral=hidden)
        except:
            if activity_id == "755600276941176913": 
                embed=simple_embed('YouTube Activity', 'YouTube','idk')
            else:
                embed=simple_embed('Discord Activity', 'Discord','idk')
            await ctx.respond(embed=embed,ephemeral=True)
    
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
