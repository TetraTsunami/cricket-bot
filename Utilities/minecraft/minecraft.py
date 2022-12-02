import asyncio
import base64
import datetime
import io
import json
import re

import aiohttp
import discord
from Utilities.format import command_embed
from mcstatus import JavaServer
from Utilities.web import async_get

embedIcon = "<:GrassBlock:924075881562009640>"


async def get_textures(uuid: int) -> list:
    """Get the textures for a given UUID."""
    res = await async_get(
        f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    )
    return json.loads(base64.b64decode(res["properties"][0]["value"]))


async def ping_server(
    server: str, plugins: bool, ctx: discord.ApplicationContext = None
) -> discord.Embed:
    """Pings a Minecraft server and returns an embed with the results."""
    try:
        target = await JavaServer.async_lookup(address=server)

        # Query the server if we're searching for plugins
        status_async = asyncio.create_task(target.async_status())
        query_async = asyncio.create_task(target.async_query()) if plugins else None

        # Wait for the tasks to finish
        status = await status_async
        query = await query_async if plugins else None

        # Build embed
        embed = command_embed(
            ctx,
            title=f"{server}",
            icon=embedIcon,
            body=f'Updated {discord.utils.format_dt(datetime.datetime.now(), "R")}',
        )
        embed.add_field(name="Version", value=status.version.name)
        embed.add_field(
            name="Players", value=f"{status.players.online}/{status.players.max}"
        )
        embed.add_field(name="Ping", value=f"{round(status.latency)} ms")

        # Remove special characters from the description, and format newlines
        description = re.sub(
            r"^\s+|§.", "", discord.utils.escape_markdown(status.description)
        )
        description = re.sub(r"\n\s*", r"\n", description)
        embed.add_field(name="Description", value=f"```{description}```", inline=False)

        # Hypixel, for instance, won't actually tell us their plugins/players even if we ask politely. They're sneaky like that, but Discord doesn't like an empty field.
        if query and query.players.names:
            # If we've already queried, may as well use the improved player list
            embed.add_field(
                name="Online",
                value="\n".join(discord.utils.escape_markdown(query.players.names)),
            )
        elif status.players.sample:
            embed.add_field(
                name="Online",
                value="\n".join(
                    discord.utils.escape_markdown(player.name)
                    for player in status.players.sample
                ),
                inline=False,
            )

        if query:
            if query.software.plugins:
                embed.add_field(name="Plugins", value="\n".join(query.software.plugins))

            # Let's try to get the server's icon
        try:
            data = base64.b64decode(status.favicon.split(",", 1)[-1])
            file = discord.File(fp=io.BytesIO(data), filename=f"{server}_icon.png")
            embed.set_thumbnail(url=f"attachment://{server}_icon.png")
        except:
            file = discord.File(
                fp="./image_gen/default_server_icon.png", filename="default_icon.png"
            )
            embed.set_thumbnail(url=f"attachment://default_icon.png")

        return embed, file
    except Exception as e:
        return (
            command_embed(ctx, server, embedIcon, f"{e.__class__.__name__}: {e}"),
            None,
        )
