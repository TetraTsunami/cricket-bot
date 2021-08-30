import os
from dotenv import load_dotenv
import logging
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import re
import sys
import socket
import io
import base64
import json
from mcstatus import MinecraftServer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG_GUILD')
cogs_dir = "cogs"

bot = commands.Bot("c!")
intents = discord.Intents(messages=True, guilds=True)
if DEBUG:
    slash = SlashCommand(bot, sync_commands=True, debug_guild=DEBUG)
else:
    slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f"*hacker voice* I\'m in. Started up as {bot.user}")
    guilds = bot.guilds
    data = {}
    for guild in guilds:
        data[guild.id] = []
        for channel in guild.channels:
            data[guild.id].append(channel.id)
    with open("result.json", "w") as file:
        json.dump(data, file, indent=4)

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))
    

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'{extension} obtained!')
        except Exception as e:
            print(f'Failed to get ahold of {extension}.')
            print(sys.exc_info())


@slash.subcommand(base="bot",
                  name="ping",
                  description="Returns info about the bot's ping")
async def bot_ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)} ms.")


@slash.subcommand(base="minecraft",
                  name="ping",
                  description="Returns info about a server",
                  options=[
                      create_option(
                          name="server",
                          description="Address of the server",
                          option_type=3,
                          required=True
                      ),
                      create_option(
                          name="plugins",
                          description="Try to list the server's plugins",
                          option_type=5,
                          required=False
                      ),
                      create_option(
                          name="persistent",
                          description="Frequently update this message with new data",
                          option_type=5,
                          required=False
                      )
                  ])
async def server_ping(ctx, server, plugins=False, persistent=False):
    await ctx.defer()
    try:
        target = MinecraftServer.lookup(server)
        status = target.status()

        embed = discord.Embed(title=server, color=0xc84268)
        embed.add_field(name="Version", value=status.version.name)
        embed.add_field(
            name="Players", value=f"{status.players.online}/{status.players.max}")
        embed.add_field(name="Ping", value=f"{round(status.latency)} ms")
        try:
            description = re.sub(r'^\s+|§.', '', status.description)
            description = re.sub(r'\n\s*', r'\n', description)
            embed.add_field(name="Description",
                            value=f"```{description}```", inline=False)
        except:
            pass
        try:
            query = target.query()
            if plugins:
                embed.add_field(name="Online", value='\n'.join(query.players.names))
                embed.add_field(name="Plugins", value='\n'.join(query.software.plugins))
            else:
                embed.add_field(name="Online", value=', '.join(query.players.names), inline=False)
        except:
            pass
        # thumbnails are hard
        try:
            data = base64.b64decode(
                status.favicon.split(',', 1)[-1])
            file = discord.File(fp=io.BytesIO(data),filename="server_favicon.png")
            embed.set_thumbnail(url="attachment://server_favicon.png")
            await ctx.send(file=file, embed=embed)
        except:
            print(sys.exc_info())
            await ctx.send(embed=embed)
    except socket.timeout:
        embed = discord.Embed(
            title=server, description="timed out :(")
        await ctx.send(embed=embed)
        print(sys.exc_info())

    except:
        embed = discord.Embed(
            title=server, description="halp am havin a stronk")
        await ctx.send(embed=embed)
        print(sys.exc_info())


logging.basicConfig(level=logging.WARNING)
bot.run(TOKEN)
