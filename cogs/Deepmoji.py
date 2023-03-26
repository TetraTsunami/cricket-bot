import asyncio
import json
import logging
import os
import random
import aiohttp

import discord
from discord.commands import Option, slash_command
from discord.ext import commands

from .utils.api.deepmoji import get_emoji
from .utils.embed import command_embed

logger = logging.getLogger("discord")

with open("configuration.json", "r") as config:
    data = json.load(config)
    deepmoji_url = (
        data["apis"]["deepmoji"]["url"] if "url" in data["apis"]["deepmoji"] else None
    )
    deepmoji_frequency = (
        data["apis"]["deepmoji"]["frequency"]
        if "frequency" in data["apis"]["deepmoji"]
        else 0.05
    )


async def testConnection():
    if deepmoji_url:
        logger.info("Testing connection to Deepmoji server")
        try:
            await get_emoji("I dislike it when bugs are loud", deepmoji_url)
            logger.info("Successfully connected to Deepmoji server")
            return True
        except Exception as e:
            logger.error(f"Connection to Deepmoji server failed with {e}")
    return False


if deepmoji_url:
    loop = asyncio.get_event_loop()
    connectionTest = loop.run_until_complete(testConnection())
else:
    logger.info("Deepmoji API not configured, disabling Deepmoji cog")


class Deepmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def deepmoji(
        self,
        ctx: discord.ApplicationContext,
        sentence: str,
        hidden: Option(bool, "Only shows results to you", required=False) = False,
    ):
        """Returns the top 10 emoji reactions for a given sentence"""
        emoji = await get_emoji(sentence, deepmoji_url, min_prob=0, results=10)
        # print(f'got {emoji} for "{message.content}"')
        page = [f"*{sentence}*"]
        for i in emoji:
            page.append(f'{i["emoji"]}: **{round(i["prob"]*100)}%**')
        await ctx.respond(
            embed=command_embed(
                title="Deepmoji results", icon="😀", body="\n".join(page), ctx=ctx
            ),
            ephemeral=hidden,
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.random() <= deepmoji_frequency:
            # 30% chance to trigger, but we have a high prob setting so it may not go off all that often
            try:
                emoji = await get_emoji(message.content, deepmoji_url, 0.20)
                if emoji:
                    await message.add_reaction(emoji[0]["emoji"])
            except aiohttp.exceptions.HTTPError as e:
                logger.warning(f'Deepmoji error "{e}" on message "{message.content}"')


def setup(bot):
    if connectionTest:
        bot.add_cog(Deepmoji(bot))
