import json
import os

import discord
from cogs.utils.embed import command_embed
from discord.commands import Option, slash_command
from discord.ext import commands


def list_cogs(cogs_dir):
    return [
        extension
        for extension in [
            f.replace(".py", "")
            for f in os.listdir(cogs_dir)
            if os.path.isfile(os.path.join(cogs_dir, f))
        ]
    ]


with open("configuration.json", "r") as config:
    data = json.load(config)
    debug_guild = data["debug_guild_id"] if "debug_guild_id" in data else None

cogs_dir = "cogs"
cogs = list_cogs(cogs_dir)


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        description="Make me say something like the grim puppetmaster you wish you could be.",
        default_permission=False,
    )
    @commands.is_owner()
    async def say(self, ctx, text: Option(str, "What you'd like to say")):
        await ctx.channel.send(content=text)
        await ctx.respond(
            "<:photothumbsup:886416067021381663><:Yeah:870075068644999248>",
            ephemeral=True,
        )

    @slash_command(description="Returns info about the bot's ping")
    async def ping(self, ctx):
        await ctx.respond(embed=command_embed(f"⚡ {round(self.bot.latency * 1000)} ms"))

    module = discord.SlashCommandGroup("module", description="Manage modules")

    @module.command(description="Loads or reloads a backend module")
    @commands.is_owner()
    async def load(
        self,
        ctx,
        module: Option(
            str,
            "Name of the cog to load",
            autocomplete=discord.utils.basic_autocomplete(cogs),
        ),
    ):
        if f"{cogs_dir}.{module}" in self.bot.extensions:
            self.bot.reload_extension(cogs_dir + "." + module)

            await self.bot.sync_commands()
            await ctx.respond(
                embed=command_embed(ctx, "Load", "Success", f"🔃 {module} reloaded"),
                ephemeral=True,
            )
        else:
            self.bot.load_extension(cogs_dir + "." + module)
            await self.bot.sync_commands()
            await ctx.respond(
                embed=command_embed(ctx, "Load", "Success", f"📥 {module} loaded"),
                ephemeral=True,
            )

    @module.command(description="Loads or reloads a backend module")
    @commands.is_owner()
    async def unload(
        self,
        ctx,
        module: Option(
            str,
            "Name of the cog to unload",
            autocomplete=discord.utils.basic_autocomplete(cogs),
        ),
    ):
        try:
            self.bot.unload_extension(cogs_dir + "." + module)
            await self.bot.sync_commands()

        except discord.ExtensionError as e:
            await ctx.respond(
                embed=command_embed(
                    ctx, "Unload", "Failure", f"{e.__class__.__name__}: {e}"
                ),
                ephemeral=True,
            )
            print(f"✗ {module} failed to unload as requested by {ctx.author}")
            print(f"→ {e.__class__.__name__}: {e}")
        else:
            await ctx.respond(
                embed=command_embed(ctx, "Unload", "Success", f"{module} unloaded"),
                ephemeral=True,
            )
            print(f"✓ {module} unloaded by {ctx.author}")


def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
