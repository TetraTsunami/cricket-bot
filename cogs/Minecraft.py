import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from mcstatus import MinecraftServer

import re
import sys
import socket
import io
import base64

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="minecraft",
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
                    name="hidden",
                    description="Only shows results to you",
                    option_type=5,
                    required=False
                ),
                create_option(
                    name="plugins",
                    description="Try to list the server's plugins",
                    option_type=5,
                    required=False
                ),
                create_option(
                    name="persistent",
                    description="(Not working yet) Frequently update this message with new data",
                    option_type=5,
                    required=False
                )
                ])
    async def minecraft_ping(self, ctx: SlashContext, server, hidden=False, plugins=False, persistent=False):
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
                await ctx.send(file=file, embed=embed,hidden=hidden)
            except:
                print(sys.exc_info())
                await ctx.send(embed=embed,hidden=hidden)
        except socket.timeout:
            embed = discord.Embed(
                title=server, description="timed out :(")
            await ctx.send(embed=embed,hidden=hidden)
            print(sys.exc_info())
        except:
            embed = discord.Embed(
                title=server, description="❌ Couldn't make funny Minecraft machine go brr, try again later")
            await ctx.send(embed=embed,hidden=hidden)
            print(sys.exc_info())
        
def setup(bot):
    bot.add_cog(Minecraft(bot))