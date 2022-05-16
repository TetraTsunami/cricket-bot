import json
import logging
import os
import sys

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

from cogs.utils.embed import simple_embed

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SUPPORT_GUILD = int(os.getenv('SUPPORT_GUILD'))
if os.getenv('DEBUG_GUILD'): DEBUG = int(os.getenv('DEBUG_GUILD'))

cogs_dir = "cogs"
activity = discord.Activity(type=discord.ActivityType.listening, name="crickets, chirp!")

intents = discord.Intents().default()
intents.messages = True
intents.guilds = True
intents.guild_messages = True

if os.getenv('DEBUG_GUILD'): bot = commands.Bot(command_prefix="c!", activity=activity, debug_guilds=[DEBUG], intents=intents)
else: bot = commands.Bot(command_prefix="c!", activity=activity, intents=intents)
discord.http.API_VERSION = 9


@bot.event
async def on_ready():
    print(f"\r✓ Logged in as {bot.user} ({bot.user.id})", end = "\n")
    if os.getenv('DEBUG_GUILD'):
        debug_guild = await bot.fetch_guild(DEBUG)
        print(f"✓ Debug guild is {debug_guild.name} ({DEBUG})")

def list_cogs():
    return [extension for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]]

if __name__ == "__main__":
    progress = 0
    total = len(list_cogs())
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        progress = progress + 1
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'{progress}/{total} {extension} loaded!')
        except Exception as e:
            print(f'{progress}/{total} {extension} broke!')
            print(f"→ {sys.exc_info()}")
        except KeyboardInterrupt:
            print('\ncya!')
            quit()
    print('\r… Modules loaded, logging in to Discord', end = "\r")
    
@bot.slash_command(description="Returns info about the bot's ping")
async def ping(ctx):
    await ctx.respond(embed=simple_embed(f"⚡ {round(bot.latency * 1000)} ms"))

module = SlashCommandGroup(
    "module",
    "Manage backend modules",
)

@module.command(description="Load a backend module", guild_ids=[SUPPORT_GUILD])
@discord.ext.commands.is_owner()
async def load(ctx, module: Option(str, "Name of the cog to load", autocomplete=discord.utils.basic_autocomplete(list_cogs()))):
    try:
        bot.load_extension(cogs_dir + "." + module)
        await bot.register_commands()
    except discord.ExtensionError as e:
        await ctx.respond(embed=simple_embed("Load",'Failure',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"✗ {module} failed to load as requested by {ctx.author}")
        print(f"→ {e.__class__.__name__}: {e}")
    else:
        await ctx.respond(embed=simple_embed("Load",'Success',f"{module} loaded"), ephemeral = True)
        print(f"✓ {module} loaded by {ctx.author}")

@module.command(description="Unload a backend module", guild_ids=[SUPPORT_GUILD])
@discord.ext.commands.is_owner()
async def unload(ctx, module: Option(str, "Name of the cog to unload", autocomplete=discord.utils.basic_autocomplete(list_cogs()))):
    try:
        bot.unload_extension(cogs_dir + "." + module)
    except discord.ExtensionError as e:
        await ctx.respond(embed=simple_embed("Unload",'Failure',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"✗ {module} failed to unload as requested by {ctx.author}")
        print(f"→ {e.__class__.__name__}: {e}")
    else:
        await ctx.respond(embed=simple_embed("Unload",'Success',f"{module} unloaded"), ephemeral = True)
        print(f"✓ {module} unloaded by {ctx.author}")
        
@module.command(description="Reload a backend module", guild_ids=[SUPPORT_GUILD])
@discord.ext.commands.is_owner()
async def reload(ctx, module: Option(str, "Name of the cog to reload", autocomplete=discord.utils.basic_autocomplete(list_cogs()))):
    try:
        bot.reload_extension(cogs_dir + "." + module) 
        # slash cog reloading is, apparently, unsupported?
        await bot.register_commands()
    except discord.ExtensionError as e:
        await ctx.respond(embed=simple_embed("Reload",'Failure',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"✗ {module} failed to reload as requested by {ctx.author}")
        print(f"→ {e.__class__.__name__}: {e}")
    else:
        await ctx.respond(embed=simple_embed("Reload",'Success',f"{module} reloaded"), ephemeral = True)
        print(f"✓ {module} reloaded by {ctx.author}")
        
bot.run(TOKEN)
