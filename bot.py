import os
from dotenv import load_dotenv
import logging
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import sys
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG_GUILD')
cogs_dir = "cogs"
activity = discord.Activity(type=discord.ActivityType.listening, name="to crickets, chirp!")

bot = commands.Bot(command_prefix="c!", activity=activity)
intents = discord.Intents(messages=True, guilds=True)
if DEBUG:
    slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, debug_guild=DEBUG, override_type = True)
else:
    slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f"*hacker voice* I\'m in. Started up as {bot.user}")

@bot.command()
async def load(ctx, extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@bot.command()
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))
    

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'{extension} loaded!')
        except Exception as e:
            print(f'Failed to get ahold of {extension}.')
            print(sys.exc_info())


@slash.subcommand(base="bot", name="ping", description="Returns info about the bot's ping")
async def bot_ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)} ms.")

# @slash.subcommand(base="bot", name="reload", description="Reloads a backend module", 
#                   options=[
#                     create_option(
#                           name="module",
#                           description="Name of the cog",
#                           option_type=3,
#                           required=True
#                       )])
# async def bot_reload(ctx, module):
#     try:
#         bot.reload_extension(module)
#     except commands.ExtensionError as e:
#         await ctx.send(f'{e.__class__.__name__}: {e}', hidden = True)
#     else:
#         await ctx.send(f"Reloaded {module}!", hidden = True)

logging.basicConfig(level=logging.WARNING)
bot.run(TOKEN)
