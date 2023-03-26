import json
import re

import discord
from cogs.utils.embed import command_embed
from cogs.utils.api.minecraft import async_get, get_textures, ping_server
from cogs.utils.view import LinkButton
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from discord.ext.commands.context import Context

# Get configuration.json
with open("configuration.json", "r") as config:
    embedIcon = json.load(config)["icons"]["minecraft"]


class MCRefreshButton(discord.ui.View):
    def __init__(
        self, server, plugins: bool = False, ctx: discord.ApplicationContext = None
    ):
        super().__init__(timeout=86400)
        self.server = server
        self.ctx = ctx
        self.plugins = plugins

    @discord.ui.button(
        label="Refresh",
        style=discord.ButtonStyle.red,
        custom_id="minecraft:refreshserver",
    )
    async def refreshButton(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        try:
            await interaction.response.defer()
            embed, file = await ping_server(self.server, self.plugins, self.ctx)
            await interaction.message.edit(embed=embed, file=file, view=self)
        except Exception as e:
            await interaction.message.edit(
                # For some reason, emojis in embed titles don't work after editing
                embed=command_embed(
                    self.ctx, self.server, embedIcon, f"{e.__class__.__name__}: {e}"
                )
            )


class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    minecraft_utils = SlashCommandGroup("minecraft", "Commands related to Minecraft.")

    @minecraft_utils.command(description="Returns info about a server")
    async def server(
        self,
        ctx: Context,
        server: Option(str, "Address of the server"),
        plugins: Option(
            bool, "Try to list the server's plugins", required=False
        ) = False,
        hidden: Option(bool, "Only shows results to you", required=False) = False,
    ):
        await ctx.defer()
        embed, file = await ping_server(server, plugins, ctx)
        view = MCRefreshButton(server, plugins, ctx) if not hidden else None
        if file:
            await ctx.respond(embed=embed, ephemeral=hidden, file=file, view=view)
        else:
            # If there's no file, there must have been an error. So no file, no refresh button.
            await ctx.respond(embed=embed, ephemeral=True)

    @minecraft_utils.command(description="Returns info about a Minecraft account")
    async def user(
        self,
        ctx: Context,
        user: Option(str, "The account's username or UUID"),
        hidden: Option(bool, "Only shows results to you", required=False) = False,
    ):
        # If given username, convert to uuid
        if re.search(
            "[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}", user
        ):
            uuid = user
        else:
            usnam = await async_get(
                f"https://api.mojang.com/users/profiles/minecraft/{user}"
            )
        # usnam.raise_for_status()
        if usnam.status_code == 204:
            return await ctx.respond(
                embed=command_embed(ctx, user, "Minecraft", f"Invalid username")
            )
        uuid = json.loads(usnam.content)["id"]
        # Get profile of uuid
        textures = await get_textures(uuid)

        view = LinkButton(
            ctx,
            buttons={
                "Skin Download": textures["textures"]["SKIN"]["url"],
                "NameMC": f"https://namemc.com/profile/{user}",
                "Hypixel": f"https://hypixel.net/player/{uuid}",
            },
            timeout=None,
        )
        # Build embed
        embed = command_embed(
            ctx,
            textures["profileName"],
            embedIcon,
            imageUrl=f"https://mc-heads.net/body/{uuid}",
        )
        embed.add_field(name="UUID", value=textures["profileId"])
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}")
        await ctx.respond(embed=embed, view=view, ephemeral=hidden)


def setup(bot):
    bot.add_cog(MinecraftCog(bot))
