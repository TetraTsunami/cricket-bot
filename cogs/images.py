import json
import logging
import re

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages

from .utils.embed import command_embed
from .utils.image import (
    TextBox,
    compress_image,
    draw_text_to_image,
    image_overlay,
    text_to_png,
    transparency,
)
from .utils.api.imgflip import Imgflip

logger = logging.getLogger("discord")

connectionTest = False


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def imgflip_setup(api):
    memes = api.get_memes()
    names = []
    for meme in memes:
        names.append(meme.name)
    page_list = []
    for idx, i in enumerate(chunks(memes, 10)):
        page_header = "These templates can be used in `/memegen generate`\n\n"
        page_contents = "\n".join(
            f"[{str(element.name)}]({str(element.url)}) ({element.box_count} boxes)"
            for element in i
        )
        page_list.append(
            discord.Embed(
                title=f"Meme Generator Page {idx+1}",
                description="".join([page_header, page_contents]),
                color=0xC84268,
            )
        )
    return {"meme_list": memes, "meme_names": names, "paginator_list": page_list}


with open("configuration.json", "r") as config:
    data = json.load(config)
    imgflip_username = (
        data["apis"]["imgflip"]["username"]
        if "username" in data["apis"]["imgflip"]
        else None
    )
    imgflip_password = (
        data["apis"]["imgflip"]["password"]
        if "password" in data["apis"]["imgflip"]
        else None
    )

if imgflip_username and imgflip_password:
    imgflip = {
        "username": imgflip_username,
        "password": imgflip_password,
    }

    logger.info("Getting Imgflip data")
    try:
        api = Imgflip(username=imgflip["username"], password=imgflip["password"])
        imgflip.update(imgflip_setup(api))
        logger.info("Successfully got Imgflip data")
        connectionTest = True
    except Exception as e:
        logger.error(f"Imgflip failed with {e}")

else:
    logger.warning("No Imgflip login specified")


class images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    image_generator = SlashCommandGroup("generator", "Generate images")

    signs = image_generator.create_subgroup("signs", "Various characters holding signs")

    imgflip_slash = image_generator.create_subgroup("imgflip", "Access the ImgFlip API")

    @image_generator.command(description="Turns your text into Minecraft text")
    async def minecraft(
        self,
        ctx,
        text: Option(str, description="What you'd like to say", required=True),
    ):
        if len(text) <= 100:
            text_to_png(
                text=f"<{ctx.author.name}> {text}", size=32, color=(255, 255, 255)
            )
            transparency()
            file = discord.File(
                fp="./work/transparent_image_gen.png",
                filename=f"{ctx.author.name}_say.png",
            )
            await ctx.respond(file=file)
        else:
            raise commands.BadArgument("The text you entered was too long.")

    @image_generator.command(description="Create a Sonic Says meme")
    async def sonicsays(
        self,
        ctx,
        text: Option(str, description="What you'd like Sonic to say", required=True),
    ):
        if len(text) <= 500:
            await ctx.defer()
            draw_text_to_image(
                TextBox(
                    pos=(44, 112),
                    dimensions=(670, 445),
                    font="./static/font/Montserrat-ExtraBold.ttf",
                    fontsize=90,
                    minFontsize=25,
                    text_color=(255, 255, 255),
                ),
                text,
                "./static/image/sonic_says_template.png",
                "./work/image_gen.png",
            )
            compress_image(700)
            file = discord.File(
                fp="./work/image_gen.png", filename=f"sonicsays_{ctx.author.name}.png"
            )
            await ctx.respond(
                embed=command_embed(ctx, "Sonic Says", imageFile=file), file=file
            )
        else:
            raise commands.BadArgument("The text you entered was too long.")

    @image_generator.command(description="Create a Shadow Says meme")
    async def shadowsays(
        self,
        ctx,
        text: Option(str, description="What you'd like Shadow to say", required=True),
    ):
        if len(text) <= 500:
            await ctx.defer()
            draw_text_to_image(
                TextBox(
                    pos=(44, 112),
                    dimensions=(670, 445),
                    font="./static/font/Montserrat-ExtraBold.ttf",
                    fontsize=90,
                    minFontsize=25,
                    text_color=(255, 255, 255),
                ),
                text,
                "./static/image/shadow_says_template.png",
                "./work/image_gen.png",
            )
            compress_image(700)
            file = discord.File(
                fp="./work/image_gen.png", filename=f"sonicsays_{ctx.author.name}.png"
            )
            await ctx.respond(
                embed=command_embed(ctx, "Shadow Says", imageFile=file), file=file
            )
        else:
            raise commands.BadArgument("The text you entered was too long.")

    @image_generator.command(description="Create a Eggman Says meme")
    async def eggmansays(
        self,
        ctx,
        text: Option(str, description="What you'd like Eggman to say", required=True),
    ):
        if len(text) <= 500:
            await ctx.defer()
            draw_text_to_image(
                TextBox(
                    pos=(44, 112),
                    dimensions=(670, 445),
                    font="./static/font/Montserrat-ExtraBold.ttf",
                    fontsize=90,
                    minFontsize=25,
                    text_color=(255, 255, 255),
                ),
                text,
                "./static/image/eggman_says_template.png",
                "./work/image_gen.png",
            )
            compress_image(700)
            file = discord.File(
                fp="./work/image_gen.png", filename=f"sonicsays_{ctx.author.name}.png"
            )
            await ctx.respond(
                embed=command_embed(ctx, "Eggman Says", imageFile=file), file=file
            )
        else:
            raise commands.BadArgument("The text you entered was too long.")

    @signs.command(description="An Inkling holding a sign")
    async def inkling(
        self,
        ctx,
        text: Option(str, description="What you'd like the sign to say", required=True),
    ):
        if len(text) <= 500:
            await ctx.defer()
            draw_text_to_image(
                TextBox(
                    pos=(756, 398),
                    dimensions=(384, 566),
                    font="./static/font/PatrickHand-Regular.ttf",
                    fontsize=100,
                    minFontsize=25,
                    text_color=(0, 0, 0),
                    angle=-10.5,
                ),
                text,
                "./static/image/inkling_sign_template.png",
                "./work/image_gen.png",
            )
            image_overlay(
                overlayPath="./static/image/inkling_sign_template_overlay.png",
                position=(639, 656),
            )
            compress_image(700)
            file = discord.File(
                fp="./static/image/image_gen.png",
                filename=f"sonicsays_{ctx.author.name}.png",
            )
            await ctx.respond(
                embed=command_embed(
                    ctx,
                    "Sign - Inkling",
                    body="Original art by: [@tsitraami](https://twitter.com/tsitraami/status/1425084920410611713?s=20&t=tHC3KIDH2ZjPvoTrouWgDg)",
                    imageFile=file,
                ),
                file=file,
            )
        else:
            raise commands.BadArgument("The text you entered was too long.")

    async def text_box_helper(ctx: discord.AutocompleteContext):
        try:
            if (
                name_to_boxes(ctx.options["meme"])
                >= int(re.sub("^box", "", ctx.focused.name))
                and not ctx.value == ""
            ):
                return [ctx.value, f"Type the contents of {ctx.focused.name}"]
            elif name_to_boxes(ctx.options["meme"]) >= int(
                re.sub("^box", "", ctx.focused.name)
            ):
                return [f"Type the contents of {ctx.focused.name}"]
            else:
                return [f"{ctx.focused.name} is not used. Press here to skip."]
        except ValueError:
            return [f'{ctx.options["meme"]} is not a valid meme.']

    @imgflip_slash.command(description="Generates a meme using the imgflip API")
    async def generate(
        self,
        ctx: discord.ApplicationContext,
        meme: Option(
            str,
            description="Select a meme format",
            autocomplete=discord.utils.basic_autocomplete(imgflip["meme_names"]),
            required=True,
        ),
        box1: Option(
            str,
            description="Text field 1",
            autocomplete=text_box_helper,
            required=False,
        ) = "",
        box2: Option(
            str,
            description="Text field 2",
            autocomplete=text_box_helper,
            required=False,
        ) = "",
        box3: Option(
            str,
            description="Text field 3",
            autocomplete=text_box_helper,
            required=False,
        ) = "",
        box4: Option(
            str,
            description="Text field 4",
            autocomplete=text_box_helper,
            required=False,
        ) = "",
        box5: Option(
            str,
            description="Text field 5",
            autocomplete=text_box_helper,
            required=False,
        ) = "",
    ):
        box_list = [box1, box2, box3, box4, box5]
        for box in box_list:
            re.sub(
                "box\d is not used. Press here to skip.|Type the contents of box\d",
                "",
                box,
            )
        box_list = [i for i in box_list if i]
        try:
            image = api.caption_image(meme=name_to_id(meme), boxes=box_list)
            meme_url = image["url"]
            await ctx.respond(
                embed=command_embed(title="ImgFlip API", imageUrl=meme_url, ctx=ctx)
            )
        except Exception as e:
            await ctx.respond(
                embed=command_embed(
                    "ImgFlip API", "Failure", f"{e.__class__.__name__}: {e}", ctx=ctx
                )
            )

    @imgflip_slash.command(description="Lists meme formats in the imgflip API")
    async def list(self, ctx):
        paginator = pages.Paginator(
            pages=imgflip["paginator_list"], show_disabled=True, show_indicator=True
        )
        await paginator.send(ctx)


def name_to_boxes(name: str):
    if re.search("\s?\d{4,}\s?", name):
        return 5
    for meme in imgflip["meme_list"]:
        if meme.name == name:
            return meme.box_count
        else:
            pass
    raise ValueError("There is no meme with provided name")


def name_to_id(name: str):
    if re.search("\s?\d{4,}\s?", name):
        return re.search("\d{4,}", name).group(0)
    for meme in imgflip["meme_list"]:
        if meme.name == name:
            return meme.id
        else:
            pass
    raise ValueError("There is no meme with provided name")


def setup(bot):
    if connectionTest:
        bot.add_cog(images(bot))
