import json
import logging
import os

import discord
import coloredlogs, logging.handlers
import os

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    release_level = data["release_level"]
    prefix = data["prefix"]
    owner_id = data["owner_id"]
    activity = data["activity"]
    debug_guild = data["debug_guild_id"] if "debug_guild_id" in data else None

# Set up logging
log = logging.getLogger("discord")

os.makedirs("logs", exist_ok=True)
fileHandler = logging.handlers.TimedRotatingFileHandler(
    filename="logs/discord.log",
    encoding="utf-8",
    when="midnight",
    backupCount=1,
)
logging.basicConfig(
    level=logging.DEBUG if release_level == "debug" else logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
    handlers=[fileHandler],
)
coloredlogs.install(
    level="INFO",
    fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
    logger=log,
)

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
# The bot
bot = discord.Bot(prefix, intents=intents, help_command=None, owner_id=owner_id)
bot.debug_guilds = [debug_guild] if debug_guild else []

# Load cogs
COGS_DIR = "Cogs"

if __name__ == "__main__":
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"Cogs.{filename[:-3]}")
                log.info(f"Module {filename} loaded")
            except Exception as e:
                log.error(f"Module {filename} failed to load. {e}")
    log.info("All modules loaded, logging in to Discord")


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user} ({bot.user.id})")
    log.warning(
        f"Using debug guilds with IDs {bot.debug_guilds}"
    ) if debug_guild else None

    log.info(discord.__version__)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=activity)
    )


bot.run(token)
