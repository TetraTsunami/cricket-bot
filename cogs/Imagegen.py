import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands

from .utils.embed import simple_embed
from .utils.image import transparency, text_on_img

class Image_gen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    image = SlashCommandGroup("image", "Generate images")
        
    @image.command(description="Turns your text into Minecraft text")
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
            
def setup(bot):
    bot.add_cog(Image_gen(bot))