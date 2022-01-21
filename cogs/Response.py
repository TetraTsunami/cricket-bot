import os
import random
import re
import time

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

from .utils.cooldown import cooldown
from .utils.deepmoji import get_emoji
from .utils.image import text_on_img, transparency

load_dotenv()
if os.getenv('DEEPMOJI_URL'):
    deepmoji_url = os.getenv('DEEPMOJI_URL')
    if os.getenv('DEEPMOJI_FREQUENCY'): deepmoji_frequency = os.getenv('DEEPMOJI_FREQUENCY')
    else: deepmoji_frequency = 0.05
    print('… Testing connection to Deepmoji server', end = "\r")
    # Test it
    try:
        get_emoji('I dislike it when bugs are loud', deepmoji_url)
        print('✓ Successfully connected to Deepmoji server')
        deepmoji = True
    except Exception as e:
        print(f'✗ Connection to Deepmoji server failed with {e}')
        deepmoji = False
    
else:
    deepmoji = False
    print('✗ No Deepmoji server specified')
# Download it at https://github.com/nolis-llc/DeepMoji-docker


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
        
        if ((re.search('(?i)^wah.?$', message.content) and message.author.id == 361660269694287883) or re.search('(?i)^wah\!\?$', message.content)):
            async with message.channel.typing():
                image = Image.open("./image_gen/wah.png")
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
            await message.channel.send(random.choice(obtain_text('wah')))
            
        if re.search('(?i)^waku.?.?waku.?$', message.content):
            await message.channel.send('hooray!')
            
        if random.random() <= deepmoji_frequency:
        # 30% chance to trigger, but we have a high prob setting so it may not go off all that often
            try:
                emoji = get_emoji(message.content, deepmoji_url, 0.12)
                # print(f'got {emoji} for "{message.content}"')
                if emoji:
                    await message.add_reaction(emoji[0]['emoji'])
            except requests.exceptions.HTTPError as e:
                print(f'Deepmoji error "{e}" on message "{message.content}"')



def obtain_text(file: str):
    content = open(f'text/{file}.txt', "r").read().split("\n")
    return content

def setup(bot):
    bot.add_cog(Fun(bot))
