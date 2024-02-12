import asyncio
import random
import re
import time

from PIL import Image

import discord
from discord.ext import commands

from .utils.image import text_to_png, transparency

cooldowns = {}


def cooldown(user, command, cooldown):
    if user not in cooldowns:
        cooldowns[user] = {}
    if command not in cooldowns[user]:
        cooldowns[user][command] = 0
    if cooldowns[user][command] < time.time():
        cooldowns[user][command] = time.time() + cooldown
        return True
    else:
        return False


class Autoresponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        SIMPLERESPONSE = [
            ["(?i)^I'm\s+back.*", "hi back"],
            ["(?i)^Hi back.*", "i'm the only one that gets to say that, clown"],
            ["(?i)^Hi the only one.*", "...stop it"],
            [
                "(?i)^hi\s*literally\s?right\s?here\s?w?o?w?.*",
                "...well, that's terribly rude of you.",
            ],
            [
                "(?i)^hey y?'?all,? scott here.?",
                "https://media.discordapp.net/attachments/377256114439585793/935748176038731906/Youre_not_Scott.png",
            ],
            [
                "(?i)cricket",
                random.choice(
                    [
                        "i'm literally right here wow",
                        "yep, that's me!",
                        "hi!!",
                        "what's up?",
                        "👀",
                        "i'm not sure i agree, but okay?",
                        "your feedback has been noted. we'll ignore that.",
                    ]
                ),
            ],
            ["(?i)^waku.?.?waku.?$", "hooray!"],
        ]
        for i in SIMPLERESPONSE:
            if re.search(i[0], message.content) and cooldown(
                message.author.id, i[0], 60
            ):
                await message.channel.send(i[1])

        if re.search("(?i)<:deadchat:\d+>", message.content) and cooldown(
            message.author.id, "deadchat", 60
        ):
            if message.channel.id == 541089040200368129:
                await message.add_reaction("<:deadchat:540541091863330816>")
            return

        if re.search("(?i)^uwu|\suwu", message.content):
            if random.randint(1, 100) < 25 and cooldown(message.author.id, "uwu", 60):
                await message.channel.send(
                    "https://media.discordapp.net/attachments/716303341822672999/768908033609695234/dontdoituwu.png"
                )
                await asyncio.sleep(0.5)
                await message.channel.send("yes, that's a threat")

        if re.search(
            "(?i)(^d.?e.{0,2}d.?c.?h.?a.?t.*|^chat\sd.?e.*d.*)", message.content
        ) and cooldown(message.author.id, "deadchat_message", 60):
            if message.guild and (message.channel.id != 541089040200368129):
                await message.channel.send(
                    "https://cdn.discordapp.com/attachments/534782089846063124/879143198197448764/objection-716514-2.mp4"
                )
                await asyncio.sleep(0.5)
                await message.channel.send(f"knock it off, {message.author.mention}")

        # Wah generator w/ Discord profile pics
        if re.search("(?i)^wah\?$", message.content) and cooldown(
            message.author.id, "img_generator", 60 * 60
        ):
            async with message.channel.typing():
                await message.author.avatar.save("./work/avatar_image_gen.png")
                im1 = Image.open("./work/avatar_image_gen.png").resize((115, 115))
                im2 = Image.open("./static/image/wah_outfit.png")
                image = Image.new("RGBA", (280, 367), (255, 255, 255, 0))
                image.paste(im1, (82, 53))
                image.alpha_composite(im2)
                image.save("./work/transparent_image_gen.png")
                file = discord.File(
                    fp="./work/transparent_image_gen.png",
                    filename=f"wah_{message.author.id}.png",
                )
                await message.channel.send(file=file)
            return

        # Wah generator w/ rotating plushie
        if re.search("(?i)^wah\!\?$", message.content) and cooldown(
            message.author.id, "img_generator", 60 * 60
        ):
            async with message.channel.typing():
                image = Image.open("./static/image/wah.png")
                angle = random.randrange(0, 360, 1)
                image.rotate(angle, expand=True, fillcolor=None).save(
                    "./work/image_gen.png", "PNG"
                )
                transparency()
                file = discord.File(
                    fp="./work/transparent_image_gen.png", filename=f"wah_{angle}.png"
                )
                await message.channel.send(file=file)
            return

        # Picture of Waluigi anti-spam measures
        if re.search("(?i)^wah.?$", message.content):
            if not cooldown(message.author.id, "wah", 10):
                await message.channel.send(
                    f"you're doing that too much, {message.author.mention}"
                )
            else:
                await message.channel.send(random.choice(read_text("wah")))


def read_text(file: str):
    content = open(f"static/text/{file}.txt", "r").read().split("\n")
    return content


def setup(bot):
    bot.add_cog(Autoresponder(bot))
