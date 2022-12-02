import asyncio
import json
import random
import re
import time


from discord.ext import commands, tasks

# JSON config of triggers and responses
with open("Utilities/text/autoresponder.json", "r") as config:
    data = json.load(config)
    SIMPLE_RESPONSE = data["simple_response"]
    PREFIX_RESPONSE = data["prefix_response"]

with open("configuration.json", "r") as config:
    data = json.load(config)
    prefix = data["prefix"]

cooldowns = {}


def cooldown(rate: int, bucket: str):
    """Implementation of an extremely simple cooldown function. Returns false if the bucket is on cooldown"""
    if bucket in cooldowns:
        if cooldowns[bucket][0] + rate < time.time():
            cooldowns[bucket] = [time.time(), rate]
            return True
        return False
    else:
        cooldowns[bucket] = [time.time(), rate]
        return True


def cooldown_left(bucket):
    if bucket in cooldowns:
        return cooldowns[bucket][0] + cooldowns[bucket][1] - time.time()
    return 0


class Autoresponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=12)
    def clear_cooldowns(self):
        for bucket in cooldowns:
            if cooldowns[bucket][0] + cooldowns[bucket][1] < time.time():
                cooldowns.pop(bucket)

    @commands.task
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # React to messages with a specific emoji in a specific channel
        if re.search("(?i)<:deadchat:\d+>", message.content) and (
            message.channel.id == 541089040200368129
        ):
            await message.add_reaction("<:deadchat:540541091863330816>")
            return

        for trigger in SIMPLE_RESPONSE:
            if re.search(trigger, message.content) and cooldown(60, message.author.id):
                await message.channel.send(
                    random.choice(SIMPLE_RESPONSE[trigger])
                    if isinstance(SIMPLE_RESPONSE[trigger], list)
                    else SIMPLE_RESPONSE[trigger]
                )
                return

        for trigger in PREFIX_RESPONSE:
            if re.search(f"{prefix}{trigger}", message.content):
                if cooldown(60, message.author.id):
                    await message.channel.send(
                        random.choice(PREFIX_RESPONSE[trigger])
                        if isinstance(PREFIX_RESPONSE[trigger], list)
                        else PREFIX_RESPONSE[trigger]
                    )
                else:
                    raise commands.CommandOnCooldown(
                        retry_after=cooldown_left(message.author.id)
                    )
                return

        if (
            message.guild
            and (message.channel.id != 541089040200368129)
            and re.search(
                "(?i)(^d.?e.*d.?chat.*|^chat d.?e.*d.*|^d.e.a?.?d..?c.h.a.t.*)",
                message.content,
            )
            and cooldown(60, message.author.id)
        ):
            await message.channel.send(
                "https://cdn.discordapp.com/attachments/534782089846063124/879143198197448764/objection-716514-2.mp4"
            ) if cooldown(60, message.author.id) else None
            await asyncio.sleep(0.5)
            await message.channel.send(f"knock it off, {message.author.mention}")


def setup(bot):
    bot.add_cog(Autoresponder(bot))
