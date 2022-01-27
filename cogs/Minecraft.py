import base64
import io
import json
import re
import datetime
import sys
import asyncio

import discord
import requests
from discord.commands import Option, SlashCommandGroup, slash_command
from discord.ext import commands
from mcstatus import MinecraftServer
from discord.ext.commands.context import Context

from .utils.embed import simple_embed

MINECRAFT_ICON="<:GrassBlock:924075881562009640>"

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

async def ping_server(server: str, plugins: bool) -> discord.Embed:
    target = MinecraftServer.lookup(server)
    
    status_async = asyncio.create_task(target.async_status())
    if plugins:
        try:
            query_async = asyncio.create_task(target.async_query(tries=1))
        except BaseException:
            pass
    #Build embed
    status = await status_async
    embed = discord.Embed(title=f'{MINECRAFT_ICON} {server}', color=0xc84268)
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
        data = base64.b64decode(
            status.favicon.split(',', 1)[-1])
        file = discord.File(fp=io.BytesIO(data),filename=f'{server}_icon.png')
        embed.set_thumbnail(url=f'attachment://{server}_icon.png')
    except:
        pass
    try:
        if plugins:
            # If we're already querying, may as well use the improved player list
            query = await query_async
            embed.add_field(name="Online", value='\n'.join(query.players.names))
            embed.add_field(name="Plugins", value='\n'.join(query.software.plugins))
        else:
            embed.add_field(name="Online", value='\n'.join(player.name for player in status.players.sample), inline=False)
    except:
        pass
    embed.set_footer(text=f"Updated {discord.utils.format_dt(datetime.datetime.now(),'R')}")
    return embed, file

# class Refresh(discord.ui.View):
#     def __init__(self, label, style, emoji):
#         super().__init__()
        
#     @discord.ui.button(label="Refresh", style=discord.ButtonStyle.blurple)
#     async def refresh(self, button: discord.ui.Button, int: discord.Interaction):
#         await int.response.send_message("Hello!", ephemeral=True)

class Refresh(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.server = ""
        self.plugins = False
        self.file = discord.File

    @discord.ui.button(
        style=discord.ButtonStyle.blurple, label="Refresh", custom_id="minecraft:refreshserver"
    )
    async def refresh(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            embed, file = await ping_server(self.server, self.plugins)
            await interaction.response.edit_message(embed=embed)
        except:
            pass
        #     await interaction.response.defer()
        #     embed, file = await ping_server(server, plugins)
        #     await interaction.response.edit_message(embed=embed, file=file)
        # except asyncio.exceptions.TimeoutError as e:
        #     await interaction.response.edit_message(embed=simple_embed(server, 'Minecraft',f'{e.__class__.__name__}: {e}'),ephemeral=True)
        # except:
        #     await interaction.response.edit_message(embed=simple_embed(server, 'Minecraft','idk'),ephemeral=True)
        #     print(sys.exc_info())
        
class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @slash_command(
    #     name="slash_command_name", description="command description!"
    # )
    # async def CommandName(self, ctx):
    #     navigator = ButtonView()  # button View <discord.ui.View>
    #     await ctx.respond("press the button.", view=navigator)

    # # for error handling
    # @CommandName.error
    # async def CommandName_error(self, ctx: Context, error):
    #     return await ctx.respond(
    #         error, ephemeral=True
    #     )  # ephemeral makes "Only you can see this" message
        
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
            embed, file = await ping_server(server, plugins)
            if not hidden:
                view = Refresh()
                view.server = server
                view.plugins = plugins
                view.file = file
            else: view = None
            await ctx.respond(embed=embed, ephemeral=hidden, file=file, view=view)
        except asyncio.exceptions.TimeoutError as e:
            await ctx.respond(embed=simple_embed(server, 'Minecraft',f'{e.__class__.__name__}: {e}'),ephemeral=True)
        except:
            await ctx.respond(embed=simple_embed(server, 'Minecraft','idk'),ephemeral=True)
            print(sys.exc_info())
        
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
        
        # Build embed
        embed = simple_embed(textures['profileName'],'Minecraft')
        embed.add_field(name='UUID', value=textures['profileId'])
        embed.add_field(name='Skin Download', value=f'[Click here to download textures]({textures["textures"]["SKIN"]["url"]})')
        embed.add_field(name="Username History", value='\n'.join(history), inline=False)
        embed.set_image(url=f'https://mc-heads.net/body/{uuid}')
        embed.set_thumbnail(url=f'https://mc-heads.net/avatar/{uuid}')
        await ctx.respond(embed=embed, ephemeral=hidden)

        
def setup(bot):
    bot.add_cog(Minecraft(bot))
