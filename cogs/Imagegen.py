import os
import re

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

from .utils.embed import simple_embed
from .utils.image import text_on_img, transparency
from .utils.imgflip import Imgflip

load_dotenv()
IMGFLIP_USERNAME = os.getenv('IMGFLIP_USERNAME')
IMGFLIP_PASSWORD = os.getenv('IMGFLIP_PASSWORD')
api = Imgflip(username=IMGFLIP_USERNAME,password=IMGFLIP_PASSWORD)
MEME_LIST = api.get_memes()
names = []
for meme in MEME_LIST:
    names.append(meme.name)
MEME_NAMES = names

class Image_gen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    memegen = SlashCommandGroup("memegen", "Generate memes")
        
    @memegen.command(description="Turns your text into Minecraft text")
    async def minecraft_say(self, ctx, text: Option(str, description="What you'd like to say", required=True)):
        if len(text) <= 100:
            try:
                text_on_img(text=f"<{ctx.author.name}> {text}", size=32, color=(255,255,255))
                transparency()
                file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"{ctx.author.name}_say.png")
                await ctx.respond(file=file)
            except:
                await ctx.respond(embed=simple_embed("Minecraft","Minecraft","idk"), ephemeral=True)
        else:
            await ctx.respond(embed=simple_embed("Minecraft","Minecraft","Length"), ephemeral=True)
        
    async def text_box_helper(ctx: discord.AutocompleteContext):
        try:
            if name_to_boxes(ctx.options['meme']) >= int(re.sub('^box','',ctx.focused.name)) and not ctx.value == '':
                return [ctx.value,f'Type the contents of {ctx.focused.name}']
            elif name_to_boxes(ctx.options['meme']) >= int(re.sub('^box','',ctx.focused.name)):
                return [f'Type the contents of {ctx.focused.name}']
            else:
                return [f'{ctx.focused.name} is not used. Press here to skip.']
        except ValueError:
            return [f'{ctx.options["meme"]} is not a valid meme.']
    
    @memegen.command(description="Generates a meme using the imgflip API")
    async def generate(
        self, 
        ctx: discord.ApplicationContext, 
        meme: Option(str, description="Select a meme format", autocomplete=discord.utils.basic_autocomplete(MEME_NAMES), required=True),
        box1: Option(str, description="Text field 1", autocomplete=text_box_helper, required=False) = '',
        box2: Option(str, description="Text field 2", autocomplete=text_box_helper, required=False) = '',
        box3: Option(str, description="Text field 3", autocomplete=text_box_helper, required=False) = '',
        box4: Option(str, description="Text field 4", autocomplete=text_box_helper, required=False) = '',
        box5: Option(str, description="Text field 5", autocomplete=text_box_helper, required=False) = '',
        ):
        box_list = [box1,box2,box3,box4,box5]
        for box in box_list: re.sub('box\d is not used. Press here to skip.|Type the contents of box\d','',box)
        box_list = [i for i in box_list if i]
        
        image = api.caption_image(meme=name_to_id(meme),boxes=box_list)
        meme_url = image['url']
        embed=discord.Embed(color=0xc84268)
        embed.set_image(url=meme_url)
        await ctx.respond(embed=embed)
        
def name_to_boxes(name: str):
    for meme in MEME_LIST:
        if meme.name == name: return meme.box_count
        else: pass
    raise ValueError('There is no meme with provided name')

def name_to_id(name: str):
    for meme in MEME_LIST:
        if meme.name == name: return meme.id
        else: pass
    raise ValueError('There is no meme with provided name')
    
def setup(bot):
    bot.add_cog(Image_gen(bot))