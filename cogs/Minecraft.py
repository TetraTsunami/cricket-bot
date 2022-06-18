import asyncio
import base64
import datetime
import io
import json
import re

import requests
from mcstatus import JavaServer

import discord
from discord.commands import Option, SlashCommandGroup, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

from .utils.embed import LinkButton, simple_embed


def get_username_history(uuid: int) -> list:
    res = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names')
    res.raise_for_status()
    history = json.loads(res.content)
    page = []
    for i in reversed(history):
        if "changedToAt" in i:
            page.append(f'**{i["name"]}** - <t:{round(i["changedToAt"]/1000)}>')
        else:
            page.append(f'**{i["name"]}**')
    return page

def get_textures(uuid: int) -> list:
    res = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    res.raise_for_status()
    return json.loads(base64.b64decode(json.loads(res.content)['properties'][0]['value']))

async def ping_server(server: str, plugins: bool, ctx: discord.ApplicationContext = None) -> discord.Embed:
    target = await JavaServer.async_lookup(address=server)
    
    
    # Query the server if we're searching for plugins
    status_async = asyncio.create_task(target.async_status())
    query_async = asyncio.create_task(target.async_query()) if plugins else None
    
    # Wait for the tasks to finish
    status = await status_async
    query = await query_async if plugins else None
    
    # Build embed
    embed = simple_embed(title=f'{server}', icon="Minecraft", body=f'Updated {discord.utils.format_dt(datetime.datetime.now(), "R")}', ctx=ctx)
    embed.add_field(name="Version", value=status.version.name)
    embed.add_field(
        name="Players", value=f"{status.players.online}/{status.players.max}")
    embed.add_field(name="Ping", value=f"{round(status.latency)} ms")
    
    # Remove special characters from the description, and format newlines
    description = re.sub(r'^\s+|§.', '', discord.utils.escape_markdown(status.description))
    description = re.sub(r'\n\s*', r'\n', description)
    embed.add_field(name="Description",
                    value=f"```{description}```", inline=False)
    
    # Hypixel, for instance, won't actually tell us their plugins/players even if we ask politely. They're sneaky like that, but Discord doesn't like an empty field.
    if query and query.players.names:
        # If we've already queried, may as well use the improved player list
        embed.add_field(name="Online", value='\n'.join(discord.utils.escape_markdown(query.players.names)))
    elif status.players.sample:
        embed.add_field(name="Online", value='\n'.join(discord.utils.escape_markdown(player.name) for player in status.players.sample), inline=False)

    
    if query:
        if query.software.plugins:
            embed.add_field(name="Plugins", value='\n'.join(query.software.plugins))
            
        # Let's try to get the server's icon
    try:
        data = base64.b64decode(
            status.favicon.split(',', 1)[-1])
        file = discord.File(fp=io.BytesIO(data),filename=f'{server}_icon.png')
        embed.set_thumbnail(url=f'attachment://{server}_icon.png')
    except:
        file = discord.File(fp="./image_gen/default_server_icon.png", filename='default_icon.png')
        embed.set_thumbnail(url=f'attachment://default_icon.png')
            
    return embed, file
    
            
class MCRefreshButton(discord.ui.View):
    def __init__(self, server, plugins: bool = False, ctx: discord.ApplicationContext = None):
        super().__init__(timeout=86400)
        self.server = server
        self.ctx = ctx
        self.plugins = plugins

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.red, custom_id="minecraft:refreshserver")
    async def refreshButton (self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            embed, file = await ping_server(self.server, self.plugins, self.ctx)
            await interaction.message.edit(embed=embed, file=file, view=self)
        except Exception as e:
            await interaction.message.edit(embed=simple_embed(self.server, 'Minecraft',f'{e.__class__.__name__}: {e}'))
            
            
      
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
        try:
            await ctx.defer()
            embed, file = await ping_server(server, plugins, ctx)
            if not hidden:
                view = MCRefreshButton(server, plugins, ctx)
            else: view = None
            await ctx.respond(embed=embed, ephemeral=hidden, file=file, view=view)
        except Exception as e:
            await ctx.respond(embed=simple_embed(server, 'Minecraft',f'{e.__class__.__name__}: {e}'),ephemeral=True)
        
    @minecraft_utils.command(description="Returns info about a Minecraft account")
    async def user(
        self, 
        ctx, 
        user: Option(str, 'The account\'s username or UUID'), 
        hidden: Option(bool, 'Only shows results to you', required=False) = False
        ):
        # If given username, convert to uuid
        if re.search("[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}",user):
            uuid = user
        else:
            try:
                usnam = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{user}")
                usnam.raise_for_status()
                if usnam.status_code == 204:
                    return await ctx.respond(embed=simple_embed(user,"Minecraft",f"Invalid username"))
                uuid = json.loads(usnam.content)['id']
            except:
                return await ctx.respond(embed=simple_embed(user,"Minecraft",f"idk"))
        # Get profile of uuid
        textures = get_textures(uuid)
        history = get_username_history(uuid)
        
        view = LinkButton(ctx, buttons={"Skin Download": textures['textures']['SKIN']['url'], "NameMC": f"https://namemc.com/profile/{user}", "Hypixel": f"https://hypixel.net/player/{uuid}"}, timeout=None)
        # Build embed
        embed = simple_embed(textures['profileName'],'Minecraft', imageUrl=f'https://mc-heads.net/body/{uuid}', ctx=ctx)
        embed.add_field(name='UUID', value=textures['profileId'])
        embed.add_field(name="Username History", value='\n'.join(history), inline=False)
        embed.set_thumbnail(url=f'https://mc-heads.net/avatar/{uuid}')
        await ctx.respond(embed=embed, view=view, ephemeral=hidden)

        
def setup(bot):
    bot.add_cog(Minecraft(bot))
