import json
import logging
import os

import discord
from discord.ext import commands

if not os.path.exists("logs"):
    os.mkdir("logs")
if not os.path.exists("work"):
    os.mkdir("work")
    
# Set up logging
fileHandler = logging.FileHandler(
    filename="logs/discord.log", encoding="utf-8", mode="w"
)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
    handlers=[fileHandler, consoleHandler],
)
logger = logging.getLogger("discord")

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]
    owner_id = data["owner_id"]
    activity = data["activity"]
    debug_guild = data["debug_guild_id"] if "debug_guild_id" in data else None

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
# The bot
class Bot(commands.Bot):
    async def close(self):
        if os.path.exists("work"):
            for f in os.listdir("work"):
                os.remove(os.path.join("work", f))
        await super().close()


bot = Bot(prefix, intents=intents, owner_id=owner_id)
if debug_guild:
    bot.debug_guilds = [debug_guild]

# Load cogs
COGS_DIRECTORY = "cogs"


def list_cogs(cogs_dir):
    return [
        extension
        for extension in [
            f.replace(".py", "")
            for f in os.listdir(cogs_dir)
            if os.path.isfile(os.path.join(cogs_dir, f))
        ]
    ]


if __name__ == "__main__":
    foundCogs = list_cogs(COGS_DIRECTORY)
    if not debug_guild and "dev" in foundCogs:
        foundCogs.remove("dev")
    logger.info(
        f"Loading cogs: {foundCogs}"
    )
    for extension in foundCogs:
        try:
            bot.load_extension(COGS_DIRECTORY + "." + extension)
            logger.debug(f"Module {extension} loaded")
        except Exception as e:
            logger.error(f"Module {extension} failed to load. {e}")
    logger.info("All modules loaded, logging in to Discord")


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} ({bot.user.id})")
    if bot.debug_guilds:
        logger.warning(f"Using debug guilds with IDs {bot.debug_guilds}")

    logger.info(discord.__version__)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=activity)
    )


bot.run(token)
