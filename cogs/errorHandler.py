import json
import logging
import traceback
from datetime import datetime, timedelta

import aiohttp
import discord
from discord import Webhook
from discord.ext import commands
from discord.ext.commands import Context

from cogs.utils.embed import command_embed

logger = logging.getLogger("discord")

with open("configuration.json", "r") as config:
    data = json.load(config)
    error_webhook_url = (
        data["error_webhook_url"] if "error_webhook_url" in data else None
    )
    support_invite = data["support_invite"] if "support_invite" in data else None


class ErrorHandlerCog(commands.Cog, name="on command error"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandOnCooldown):
            expirationTime = datetime.now() + timedelta(seconds=error.retry_after)
            text = f"This command is on a cooldown that expires {discord.utils.format_dt(expirationTime, 'R')}"
            await ctx.respond(
                embed=command_embed(ctx, title=ctx.command.name, icon="⏳", body=text),
                ephemeral=True,
            )
            return

        # If we can't handle this, log the error & give the user a response
        if error_webhook_url:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(error_webhook_url, session=session)

                e = (
                    discord.Embed(
                        title="Command Error",
                        description=f"```{''.join(traceback.format_exception(type(error), error, error.__traceback__))}```",
                        color=0xFF0000,
                    )
                    .add_field(name="Command", value=f"/{ctx.command.qualified_name}")
                    .add_field(name="User", value=f"{ctx.author} ({ctx.author.id})")
                    .add_field(name="Guild", value=f"{ctx.guild} ({ctx.guild.id})")
                )

                await webhook.send(embed=e)

        logger.error(
            f"Ignoring exception in command {ctx.command}, see log for more info."
        )
        logger.debug(
            f"Uncaught exception in command {ctx.command} invoked by {ctx.author}.",
            exc_info=(type(error), error, error.__traceback__),
        )

        logString = (
            f", and the error has been logged."
            if error_webhook_url
            else "."
        )
        inviteString = (
            f"or join my [support server]({support_invite}) in the meantime."
            if support_invite
            else "okay?"
        )
        await ctx.respond(
            embed=command_embed(
                ctx,
                title=f"/{ctx.command.qualified_name}",
                icon="❌",
                body=f"Something went terribly wrong while executing the command /{ctx.command.qualified_name}{logString} Try again in a little while, {inviteString} ```{error}```"
            ),
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
