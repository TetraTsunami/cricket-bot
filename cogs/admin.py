import logging
import os

from dotenv import load_dotenv

import discord
from discord.commands import Option, slash_command
from discord.ext import commands

from .utils.embed import simple_embed

load_dotenv()
if os.getenv('SUPPORT_SERVER'): SUPPORT_SERVER = int(os.getenv('SUPPORT_SERVER'))

logger = logging.getLogger('discord')

def list_cogs(cogs_dir):
    return [extension for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]]
    
cogs_dir = "cogs"
cogs = list_cogs(cogs_dir)

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
        
    module = discord.SlashCommandGroup('module', description="Manage modules") 
    
    @module.command(description="Loads or reloads a backend module")
    @discord.ext.commands.is_owner()
    async def load(self, ctx, module: Option(str, "Name of the cog to load", autocomplete=discord.utils.basic_autocomplete(cogs))):
        try:
            if f"{cogs_dir}.{module}" in self.bot.extensions:
                self.bot.reload_extension(cogs_dir + "." + module)
                await self.bot.sync_commands()
                await ctx.respond(embed=simple_embed("Load",'Success',f"🔃 {module} reloaded", ctx=ctx), ephemeral = True)
                print(f"✓ {module} reloaded by {ctx.author}")
            else:
                self.bot.load_extension(cogs_dir + "." + module)
                await self.bot.sync_commands()
                await ctx.respond(embed=simple_embed("Load",'Success',f"📥 {module} loaded", ctx=ctx), ephemeral = True)
                print(f"✓ {module} loaded by {ctx.author}")
        except Exception as e:
            await ctx.respond(embed=simple_embed("Load",'Failure',f'{e.__class__.__name__}: {e}', ctx=ctx), ephemeral = True)
            print(f"✗ {module} failed to load as requested by {ctx.author}")
            print(f"→ {e.__class__.__name__}: {e}")
            
    @module.command(description="Loads or reloads a backend module")
    @discord.ext.commands.is_owner()
    async def unload(self, ctx, module: Option(str, "Name of the cog to unload", autocomplete=discord.utils.basic_autocomplete(cogs))):
        try:
            self.bot.unload_extension(cogs_dir + "." + module)
            await self.bot.sync_commands()
            
        except discord.ExtensionError as e:
            await ctx.respond(embed=simple_embed("Unload",'Failure',f'{e.__class__.__name__}: {e}', ctx=ctx), ephemeral = True)
            print(f"✗ {module} failed to unload as requested by {ctx.author}")
            print(f"→ {e.__class__.__name__}: {e}")
        else:
            await ctx.respond(embed=simple_embed("Unload",'Success',f"{module} unloaded", ctx=ctx), ephemeral = True)
            print(f"✓ {module} unloaded by {ctx.author}")
    

def setup(bot):
    bot.add_cog(Admin(bot))
