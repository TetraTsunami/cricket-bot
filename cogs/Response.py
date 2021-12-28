import random
import re
import time

import discord
from discord.ext import commands
from PIL import Image

from .utils.cooldown import cooldown
from .utils.image import transparency, text_on_img


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if re.search('(?i)<:deadchat:\d+>', message.content):
            if message.channel.id == 541089040200368129:
                await message.add_reaction("<:deadchat:540541091863330816>")
            return
            
        if re.search('(?i)^I\'m.+back.*', message.content):
            await message.channel.send('hi back')

        if re.search('(?i)^Hi back.*', message.content):
            await message.channel.send('i\'m the only one that gets to say that, clown')

        if re.search('(?i)^Hi the only one.*', message.content):
            await message.channel.send('...')
            time.sleep(0.5)
            await message.channel.send('stop it')

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
                # print(message.author.roles)
                # we want to respect pronouns, so if someone has a role implying otherwise, we'll try not to call them a man.
                result = []
                for role in message.author.roles:
                    if re.search('(?i).*She.*|.*They.*', role.name):
                        result.append(role.name)
                if result:
                    await message.channel.send('knock it off, clown')
                else:
                    await message.channel.send('knock it off, funnyman')

        if re.search('(?i)cricket', message.content) and cooldown(message.guild.id, 'cricket', 60*60*24) == True:
            await message.channel.send('i\'m literally right here wow')

        if re.search('(?i)^wah\?$', message.content):
            async with message.channel.typing():
                await message.author.avatar.url.save("avatar_image_gen.png")
                im1 = Image.open('avatar_image_gen.png').resize((115,115))
                im2 = Image.open('wah_outfit.png')
                image = Image.new("RGBA", (280,367), (255, 255, 255, 0))
                image.paste(im1,(82,53))
                image.alpha_composite(im2)
                image.save('./image_gen/transparent_image_gen.png')
                file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"wah_{message.author.id}.png") 
                await message.channel.send(file=file)
            return
        
        if (re.search('(?i)^wah.?$', message.content) and message.author.id == 361660269694287883):
            async with message.channel.typing():
                image = Image.open("wah.png")
                angle=random.randrange(0,360,1)
                image.rotate(angle,expand=True,fillcolor=None).save("./image_gen/image_gen.png", "PNG")
                transparency()
                file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"wah_{angle}.png") 
                await message.channel.send(file=file)
            return
            
        if re.search('(?i)^wah.?$', message.content) and not cooldown(message.author.id, 'wah', 10, write=False):
            if not cooldown(message.guild.id, 'spam', 120):
                if cooldown(message.guild.id, 'guild.wah', 60*60*24):
                    try:
                        text_on_img(text=f"{message.author.name} spammed and ruined it for everyone", size=32)
                        transparency()
                        file = discord.File(fp="./image_gen/transparent_image_gen.png", filename=f"{message.author.name}_ruined_it.png")
                        await message.channel.send(file=file)
                    except:
                        await message.channel.send(f"{message.author.name} spammed and ruined it for everyone")
            else:
                responses = ["https://media.discordapp.net/attachments/716303341822672999/886051336519549019/no.jpg", "please stop spamming lol","spamming is sus. you're spamming. <:stevesmug:727202674587467857>", "i'm beginning to think y'all may have a problem","no wah. instead here's a turtle with a hat <:turtleyeehaw:873380927735205958>", f"y'all treat me like a wah machine but *i'm so much more, {message.author.mention}*", "go ask someone else for waluigi pics", "no.", "wah?"]
                await message.channel.send(random.choice(responses))
                    
        if re.search('(?i)^wah.?$', message.content) and cooldown(message.author.id, 'wah', 10) and cooldown(message.guild.id, 'guild.wah', 60*60*24, write=False) == True:
            Waluigi = ['https://cdn.discordapp.com/attachments/668622610543935498/870716564779958352/paeewgo7i9u312.jpg', 'https://cdn.discordapp.com/attachments/716303341822672999/880179579044647002/waah.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179566738542652/waahh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179530482987068/waaaaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179525512728626/waa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179527131750400/waaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179524086673448/wa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179522283114516/wahhhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179520253100093/wahhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179517681987594/wah.png', 'https://media.discordapp.net/attachments/683111565230342188/885962413457952768/image0.jpg','https://cdn.discordapp.com/attachments/716303341822672999/886000782997086249/w_a_a.png','https://media.discordapp.net/attachments/716303341822672999/886002244439380039/wa.webp','https://media.discordapp.net/attachments/534781603860316160/886044958547644466/unknown.png','https://media.discordapp.net/attachments/716303341822672999/886052239163129916/e07.png','https://media.discordapp.net/attachments/716303341822672999/886052462023299112/fxx8gwhs.png','https://cdn.discordapp.com/attachments/716303341822672999/886052535025160242/67c.png','https://cdn.discordapp.com/attachments/716303341822672999/886052735668084826/c2fy9ie1.png', 'https://cdn.discordapp.com/attachments/883874626848063531/923019291119464448/yah.jpg', 'https://cdn.discordapp.com/attachments/883874626848063531/923019291446640750/wahhhhhh.jpg', 'https://cdn.discordapp.com/attachments/883874626848063531/923019291891232768/wahoo.jpg', 'https://cdn.discordapp.com/attachments/883874626848063531/923019292096749568/waht.jpg', 'https://cdn.discordapp.com/attachments/883874626848063531/923019292293865482/wahwah.jpg']
            await message.channel.send(random.choice(Waluigi))

def setup(bot):
    bot.add_cog(Fun(bot))
