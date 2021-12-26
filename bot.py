import os
from dotenv import load_dotenv
from cogs.utils.embed import simple_embed
import logging
import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup, Permission
import sys
import json

print("~~~~ Cricket! ~~~~")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if os.getenv('DEBUG_GUILD'): DEBUG = int(os.getenv('DEBUG_GUILD'))
if os.getenv('SUPPORT_GUILD'): SUPPORT_GUILD = int(os.getenv('SUPPORT_GUILD'))

cogs_dir = "cogs"
activity = discord.Activity(type=discord.ActivityType.listening, name="crickets, chirp!")

bot = commands.Bot(command_prefix="c!", activity=activity, debug_guilds=[DEBUG])
intents = discord.Intents(messages=True, guilds=True)


@bot.event
async def on_ready():
    print(f"✓ Logged in as {bot.user} ({bot.user.id})")
    if DEBUG:
        debug_guild = await bot.fetch_guild(DEBUG)
        print(f"✓ Debug guild is {debug_guild.name} ({DEBUG})")
    print("~~~~~ <コ:彡 ~~~~~")

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

@bot.slash_command(description="Returns info about the bot's ping")
async def ping(ctx):
    await ctx.respond(embed=simple_embed(f"⚡ {round(bot.latency * 1000)} ms"))

module = bot.create_group(
    "module",
    "Manage backend modules"
    # permissions=[
    #     Permission(
    #         bot.owner_id, 2, True
    #     )
    # ],
)
        
@module.command(description="Load a backend module", guild_ids=[SUPPORT_GUILD])
async def load(ctx, module: Option(str, "Name of the cog to load", autocomplete=discord.utils.basic_autocomplete(list_cogs()))):
    try:
        bot.load_extension(cogs_dir + "." + module)
        await bot.register_commands()
    except discord.ExtensionError as e:
        await ctx.respond(embed=simple_embed("Load",'Failure',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"✗ {module} failed to load as requested by {ctx.author}")
        print(f"→ {e.__class__.__name__}: {e}")
    except discord.HTTPException as e:
        await ctx.respond(embed=simple_embed("Reload",'Warning',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"? {module} maybe loaded as requested by {ctx.author}?")
        print(f"→ {e.__class__.__name__}: {e}")
    else:
        await ctx.respond(embed=simple_embed("Load",'Success',f"{module} loaded"), ephemeral = True)
        print(f"✓ {module} loaded by {ctx.author}")

@module.command(description="Unload a backend module", guild_ids=[SUPPORT_GUILD])
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
async def reload(ctx, module: Option(str, "Name of the cog to reload", autocomplete=discord.utils.basic_autocomplete(list_cogs()))):
    try:
        bot.reload_extension(cogs_dir + "." + module)
        await bot.register_commands()
    except discord.ExtensionError as e:
        await ctx.respond(embed=simple_embed("Reload",'Failure',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"✗ {module} failed to reload as requested by {ctx.author}")
        print(f"→ {e.__class__.__name__}: {e}")
    except discord.HTTPException as e:
        await ctx.respond(embed=simple_embed("Reload",'Warning',f'{e.__class__.__name__}: {e}'), ephemeral = True)
        print(f"? {module} maybe reloaded as requested by {ctx.author}?")
        print(f"→ {e.__class__.__name__}: {e}")
    else:
        await ctx.respond(embed=simple_embed("Reload",'Success',f"{module} reloaded"), ephemeral = True)
        print(f"✓ {module} reloaded by {ctx.author}")

logging.basicConfig(level=logging.WARNING)
bot.run(TOKEN)
