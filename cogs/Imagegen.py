import logging
import os
import re

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv

from .utils.embed import simple_embed
from .utils.image import (TextBox, compress_image, draw_text_to_image,
                          image_overlay, text_to_png, transparency)
from .utils.imgflip import Imgflip

logger = logging.getLogger('discord')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def imgflip_setup(api):
    memes = api.get_memes()
    names = []
    for meme in memes:
        names.append(meme.name)
    page_list = []
    for idx, i in enumerate(chunks(memes, 10)):
        page_header = 'These templates can be used in `/memegen generate`\n\n'
        page_contents = '\n'.join(
            f'[{str(element.name)}]({str(element.url)}) ({element.box_count} boxes)' for element in i)
        page_list.append(discord.Embed(
            title=f"Meme Generator Page {idx+1}", description=''.join([page_header, page_contents]), color=0xc84268))
    return {'meme_list': memes,
            'meme_names': names,
            'paginator_list': page_list
            }


load_dotenv()
if os.getenv('IMGFLIP_USERNAME') and os.getenv('IMGFLIP_PASSWORD'):
    imgflip = {
        'username': os.getenv('IMGFLIP_USERNAME'),
        'password': os.getenv('IMGFLIP_PASSWORD'),
    }

    print('\r… Getting Imgflip data', end="\r")
    # Test it
    try:
        api = Imgflip(username=imgflip['username'],
                      password=imgflip['password'])
        imgflip.update(imgflip_setup(api))
        print('✓ Successfully got Imgflip data')
    except Exception as e:
        print(f'✗ Imgflip failed with {e}')

else:
    print('✗ No Imgflip login specified')


class Image_gen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    imagegen = SlashCommandGroup("generator", "Generate images")

    signs = imagegen.create_subgroup(
        "signs", "Various characters holding signs")

    imgflip_slash = imagegen.create_subgroup(
        "imgflip", "Access the ImgFlip API")

    @imagegen.command(description="Turns your text into Minecraft text")
    async def minecraft(self, ctx, text: Option(str, description="What you'd like to say", required=True)):
        if len(text) <= 100:
            try:
                text_to_png(text=f"<{ctx.author.name}> {text}",
                            size=32, color=(255, 255, 255))
                transparency()
                file = discord.File(
                    fp="./image_gen/transparent_image_gen.png", filename=f"{ctx.author.name}_say.png")
                await ctx.respond(file=file)
            except:
                logger.debug(
                    f"Error in /memegen minecraft (invoked by {ctx.author.name}): {e}")
                await ctx.respond(embed=simple_embed("Minecraft", "Minecraft", "idk", ctx=ctx), ephemeral=True)
        else:
            await ctx.respond(embed=simple_embed("Minecraft", "Minecraft", "Length", ctx=ctx), ephemeral=True)

    @imagegen.command(description="Create a Sonic Says meme")
    async def sonicsays(self, ctx, text: Option(str, description="What you'd like Sonic to say", required=True)):
        if len(text) <= 500:
            try:
                await ctx.defer()
                draw_text_to_image(TextBox(pos=(44, 112), dimensions=(670, 445), font="./image_gen/Montserrat-ExtraBold.ttf", fontsize=90,
                                   minFontsize=25, text_color=(255, 255, 255)), text, "./image_gen/sonic_says_template.png", "./image_gen/image_gen.png")
                compress_image(700)
                file = discord.File(
                    fp="./image_gen/image_gen.png", filename=f"sonicsays_{ctx.author.name}.png")
                await ctx.respond(embed=simple_embed("Sonic Says", imageFile=file, ctx=ctx), file=file)
            except Exception as e:
                logger.debug(
                    f"Error in /generate sonicsays (invoked by {ctx.author.name}): {e}")
                await ctx.respond(embed=simple_embed("Failure", "Sonicsays", "idk", ctx=ctx), ephemeral=True)
        else:
            await ctx.respond(embed=simple_embed("Failure", "Sonicsays", "Length", ctx=ctx), ephemeral=True)
            
    @imagegen.command(description="Create a Shadow Says meme")
    async def shadowsays(self, ctx, text: Option(str, description="What you'd like Shadow to say", required=True)):
        if len(text) <= 500:
            try:
                await ctx.defer()
                draw_text_to_image(TextBox(pos=(44, 112), dimensions=(670, 445), font="./image_gen/Montserrat-ExtraBold.ttf", fontsize=90,
                                   minFontsize=25, text_color=(255, 255, 255)), text, "./image_gen/shadow_says_template.png", "./image_gen/image_gen.png")
                compress_image(700)
                file = discord.File(
                    fp="./image_gen/image_gen.png", filename=f"sonicsays_{ctx.author.name}.png")
                await ctx.respond(embed=simple_embed("Shadow Says", imageFile=file, ctx=ctx), file=file)
            except Exception as e:
                logger.debug(
                    f"Error in /generate shadowsays (invoked by {ctx.author.name}): {e}")
                await ctx.respond(embed=simple_embed("Failure", "Shadowsays", "idk", ctx=ctx), ephemeral=True)
        else:
            await ctx.respond(embed=simple_embed("Failure", "Shadowsays", "Length", ctx=ctx), ephemeral=True)

    @signs.command(description="An Inkling holding a sign")
    async def inkling(self, ctx, text: Option(str, description="What you'd like the sign to say", required=True)):
        if len(text) <= 500:
            try:
                await ctx.defer()
                draw_text_to_image(TextBox(pos=(756, 398), dimensions=(384, 566), font="./image_gen/PatrickHand-Regular.ttf", fontsize=100,
                                           minFontsize=25, text_color=(0, 0, 0), angle=-10.5), text, "./image_gen/inkling_sign_template.png", "./image_gen/image_gen.png")
                image_overlay(overlayPath="./image_gen/inkling_sign_template_overlay.png",
                              position=(639, 656))
                compress_image(700)
                file = discord.File(
                    fp="./image_gen/image_gen.png", filename=f"sonicsays_{ctx.author.name}.png")
                await ctx.respond(embed=simple_embed("Sign - Inkling", body="Original art by: [@tsitraami](https://twitter.com/tsitraami/status/1425084920410611713?s=20&t=tHC3KIDH2ZjPvoTrouWgDg)", imageFile=file, ctx=ctx), file=file)
            except Exception as e:
                logger.debug(
                    f"Error in /generate signs inkling (invoked by {ctx.author.name}): {e}")
                await ctx.respond(embed=simple_embed("Failure", "Sign - Inkling", "idk", ctx=ctx), ephemeral=True)
        else:
            await ctx.respond(embed=simple_embed("Failure", "Sign - Inkling", "Length", ctx=ctx), ephemeral=True)

    async def text_box_helper(ctx: discord.AutocompleteContext):
        try:
            if name_to_boxes(ctx.options['meme']) >= int(re.sub('^box', '', ctx.focused.name)) and not ctx.value == '':
                return [ctx.value, f'Type the contents of {ctx.focused.name}']
            elif name_to_boxes(ctx.options['meme']) >= int(re.sub('^box', '', ctx.focused.name)):
                return [f'Type the contents of {ctx.focused.name}']
            else:
                return [f'{ctx.focused.name} is not used. Press here to skip.']
        except ValueError:
            return [f'{ctx.options["meme"]} is not a valid meme.']

    @imgflip_slash.command(description="Generates a meme using the imgflip API")
    async def generate(
        self,
        ctx: discord.ApplicationContext,
        meme: Option(str, description="Select a meme format", autocomplete=discord.utils.basic_autocomplete(imgflip['meme_names']), required=True),
        box1: Option(str, description="Text field 1",
                     autocomplete=text_box_helper, required=False) = '',
        box2: Option(str, description="Text field 2",
                     autocomplete=text_box_helper, required=False) = '',
        box3: Option(str, description="Text field 3",
                     autocomplete=text_box_helper, required=False) = '',
        box4: Option(str, description="Text field 4",
                     autocomplete=text_box_helper, required=False) = '',
        box5: Option(str, description="Text field 5",
                     autocomplete=text_box_helper, required=False) = '',
    ):
        box_list = [box1, box2, box3, box4, box5]
        for box in box_list:
            re.sub(
                'box\d is not used. Press here to skip.|Type the contents of box\d', '', box)
        box_list = [i for i in box_list if i]
        try:
            image = api.caption_image(meme=name_to_id(meme), boxes=box_list)
            meme_url = image['url']
            await ctx.respond(embed=simple_embed(title="ImgFlip API", imageUrl=meme_url, ctx=ctx))
        except Exception as e:
            await ctx.respond(embed=simple_embed('ImgFlip API', 'Failure', f'{e.__class__.__name__}: {e}', ctx=ctx))

    @imgflip_slash.command(description="Lists meme formats in the imgflip API")
    async def list(self, ctx):
        paginator = pages.Paginator(
            pages=imgflip['paginator_list'], show_disabled=True, show_indicator=True)
        await paginator.send(ctx)


def name_to_boxes(name: str):
    if re.search("\s?\d{4,}\s?", name):
        return 5
    for meme in imgflip['meme_list']:
        if meme.name == name:
            return meme.box_count
        else:
            pass
    raise ValueError('There is no meme with provided name')


def name_to_id(name: str):
    if re.search("\s?\d{4,}\s?", name):
        return re.search("\d{4,}", name).group(0)
    for meme in imgflip['meme_list']:
        if meme.name == name:
            return meme.id
        else:
            pass
    raise ValueError('There is no meme with provided name')


def setup(bot):
    bot.add_cog(Image_gen(bot))
