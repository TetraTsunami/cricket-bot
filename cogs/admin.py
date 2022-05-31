import logging
import os

import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv

from .utils.embed import simple_embed

load_dotenv()
if os.getenv('SUPPORT_SERVER'): SUPPORT_SERVER = int(os.getenv('SUPPORT_SERVER'))

logger = logging.getLogger('discord')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @slash_command(description="Make me say something like the grim puppetmaster you wish you could be.", default_permission=False) 
    @discord.ext.commands.is_owner()
    async def say(self, ctx, text: Option(str, 'What you\'d like to say')):
        await ctx.channel.send(content=text)
        await ctx.respond("<:photothumbsup:886416067021381663><:Yeah:870075068644999248>",ephemeral=True)
        
    @slash_command(description="Returns info about the bot's ping")
    async def ping(self, ctx):
        await ctx.respond(embed=simple_embed(f"⚡ {round(self.bot.latency * 1000)} ms"))
    

def setup(bot):
    bot.add_cog(Admin(bot))
