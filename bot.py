import json
import logging
import os

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

from cogs.utils.embed import simple_embed

logger = logging.getLogger('discord')

loggingConsole = logging.StreamHandler()
loggingConsole.setLevel(logging.INFO)
logger.addHandler(loggingConsole)

loggingFile = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
loggingFile.setLevel(logging.DEBUG)
loggingFile.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(loggingFile)

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

bot = commands.Bot(command_prefix="c!", activity=activity, intents=intents)
if os.getenv('DEBUG_GUILD'): bot.debug_guilds=[DEBUG]


@bot.event
async def on_ready():
    logger.info(f"\r✓ Logged in as {bot.user} ({bot.user.id})")
    if bot.debug_guilds: print(f"✓ Debug guild ID is {DEBUG}")
        

def list_cogs():
    return [extension for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]]

if __name__ == "__main__":
    progress = 0
    total = len(list_cogs())
    for extension in list_cogs():
        progress = progress + 1
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'{progress}/{total} {extension} loaded')
        except Exception as e:
            print(f'{progress}/{total} {extension} failed to load')
            print(f"→ {e.__class__.__name__}: {e}")
    logger.info('\r… Modules loaded, logging in to Discord')
    
        
bot.run(TOKEN)
