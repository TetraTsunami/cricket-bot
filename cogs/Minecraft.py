import base64
import io
import re
import socket
import sys

import discord
from discord.commands import Option, SlashCommandGroup, slash_command
from discord.ext import commands
from mcstatus import MinecraftServer

from .utils.embed import simple_embed


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    minecraft_utils = SlashCommandGroup("minecraft", "Commands related to Minecraft.")
    
    @minecraft_utils.command(description="Returns info about a server")
    async def ping(
        self, 
        ctx, 
        server: Option(str, 'Address of the server'), 
        plugins: Option(bool, 'Try to list the server\'s plugins', required=False) = False,
        hidden: Option(bool, 'Only shows results to you', required=False) = False
        # persistent=False
        ):
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
            try:
                data = base64.b64decode(
                    status.favicon.split(',', 1)[-1])
                file = discord.File(fp=io.BytesIO(data),filename=f'{server}_icon.png')
                embed.set_thumbnail(url=f'attachment://{server}_icon.png')
                await ctx.respond(file=file, embed=embed,ephemeral=hidden)
            except:
                print(sys.exc_info())
                await ctx.send(embed=embed,hidden=hidden)
        except socket.timeout as e:
            await ctx.send(embed=simple_embed(server, 'Minecraft',f'{e.__class__.__name__}: {e}'),ephemeral=hidden)
        except:
            await ctx.respond(embed=simple_embed(server, 'Minecraft','idk'),ephemeral=hidden)
            print(sys.exc_info())
        
def setup(bot):
    bot.add_cog(Minecraft(bot))
