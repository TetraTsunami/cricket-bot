import random
import re
import time

import discord
from discord.ext import commands
from PIL import Image

from .utils.cooldown import cooldown
from .utils.image import text_to_png, transparency

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        SIMPLERESPONSE = [
            ['(?i)^I\'m.+back.*', 'hi back', 60],
            ['(?i)^Hi back.*', 'i\'m the only one that gets to say that, clown', 60],
            ['(?i)^Hi the only one.*', '...stop it', 60],
            ['(?i)^hi\s*literally\s?right\s?here\s?w?o?w?.*', '...well, that\'s terribly rude of you.', 60],
            ['(?i)^hey y?\'?all,? scott here.?', 'https://media.discordapp.net/attachments/377256114439585793/935748176038731906/Youre_not_Scott.png', 60],
            ['(?i)cricket', random.choice(['i\'m literally right here wow','yep, that\'s me!','hi!!','wazzaap','👀','i\'m not sure i agree, but okay?','your feedback has been noted. we\'ll ignore that.']), 60],
            ['(?i).*bread.*', '<:loaf_slice:960335609589796935>', 60],
            ['(?i).*loaf.*', '<:loaf_end:960335609430442045>', 60],
            ['(?i)^waku.?.?waku.?$', 'hooray!', 60]
        ]
        for i in SIMPLERESPONSE:
            if re.search(i[0], message.content) and cooldown(message.author.id, i[0], i[2]): await message.channel.send(i[1])
            
        if re.search('(?i)<:deadchat:\d+>', message.content):
            if message.channel.id == 541089040200368129:
                await message.add_reaction("<:deadchat:540541091863330816>")
            return

        if re.search('(?i)\suwu', message.content):
            if random.choice([0, 0, 0, 1]):
                await message.channel.send('https://media.discordapp.net/attachments/716303341822672999/768908033609695234/dontdoituwu.png')
                time.sleep(0.5)
                await message.channel.send('yes, that\'s a threat')

        if re.search('(?i)(^d.?e.*d.?chat.*|^chat d.?e.*d.*|^d.e.a?.?d..?c.h.a.t.*)', message.content):
            if (message.guild):
                if message.channel.id == 541089040200368129:
                    # don't react to :deadchat: in #deadchat 
                    return
                await message.channel.send('https://cdn.discordapp.com/attachments/534782089846063124/879143198197448764/objection-716514-2.mp4')
                time.sleep(0.5)
                await message.channel.send(f'knock it off, {message.author.mention}')

        #Wah generator w/ Discord profile pics
        if re.search('(?i)^wah\?$', message.content) and cooldown(message.author.id, 'wah_generator', 60*60):
            async with message.channel.typing():
                await message.author.avatar.save("./image_gen/avatar_image_gen.png")
                im1 = Image.open('./image_gen/avatar_image_gen.png').resize((115,115))
                im2 = Image.open('./image_gen/wah_outfit.png')
                image = Image.new("RGBA", (280,367), (255, 255, 255, 0))
                image.paste(im1,(82,53))
                image.alpha_composite(im2)
                image.save('./image_gen/transparent_image_gen.png')
                file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"wah_{message.author.id}.png") 
                await message.channel.send(file=file)
            return
        
        #Wah generator w/ rotating plushie
        if ((re.search('(?i)^wah.?$', message.content) and message.author.id == 361660269694287883) or re.search('(?i)^wah\!\?$', message.content)):
            async with message.channel.typing():
                image = Image.open("./image_gen/wah.png")
                angle=random.randrange(0,360,1)
                image.rotate(angle,expand=True,fillcolor=None).save("./image_gen/image_gen.png", "PNG")
                transparency()
                file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"wah_{angle}.png") 
                await message.channel.send(file=file)
            return
            
        #Picture of Waluigi anti-spam measures
        if re.search('(?i)^wah.?$', message.content) and not cooldown(message.author.id, 'wah', 10, write=False):
            if not cooldown(message.guild.id, 'spam', 120):
                if cooldown(message.guild.id, 'guild.wah', 60*60*24):
                    try:
                        text_to_png(text=f"{message.author.name} spammed and ruined it for everyone", size=32)
                        transparency()
                        file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"{message.author.name}_ruined_it.png")
                        await message.channel.send(file=file)
                    except:
                        await message.channel.send(f"{message.author.name} spammed and ruined it for everyone")
            else:
                responses = ["https://media.discordapp.net/attachments/716303341822672999/886051336519549019/no.jpg", "please stop spamming lol","spamming is sus. you're spamming. <:stevesmug:727202674587467857>", "i'm beginning to think y'all may have a problem","no wah. instead here's a turtle with a hat <:turtleyeehaw:873380927735205958>", f"y'all treat me like a wah machine but *i'm so much more, {message.author.mention}*", "go ask someone else for waluigi pics", "no.", "wah?"]
                await message.channel.send(random.choice(responses))
                
        #Picture of Waluigi
        if re.search('(?i)^wah.?$', message.content) and cooldown(message.author.id, 'wah', 10) and cooldown(message.guild.id, 'guild.wah', 60*60*24, write=False) == True:
            await message.channel.send(random.choice(obtain_text('wah')))
            


def obtain_text(file: str):
    content = open(f'text/{file}.txt', "r").read().split("\n")
    return content

def setup(bot):
    bot.add_cog(Fun(bot))
