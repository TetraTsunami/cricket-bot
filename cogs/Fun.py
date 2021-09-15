import json
import os
import random
import re
import sys
import time

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from PIL import Image, ImageDraw, ImageFont


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
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

            if re.search('(?i)^wah.', message.content) and not cooldown(message.author.id, 'wah', 15, write=False):
                if not cooldown(message.guild.id, 'spam', 120):
                    if cooldown(message.guild.id, 'guild.wah', 60*60*24):
                        try:
                            text_on_img(text=f"{message.author.name} spammed and ruined it for everyone", size=32)
                            transparency()
                            file = discord.File(fp="transparent_image_gen.png", filename=f"{message.author.name}_ruined_it.png")
                            await message.channel.send(file=file)
                        except:
                            await message.channel.send(f"{message.author.name} spammed and ruined it for everyone")
                else:
                    responses = ["https://media.discordapp.net/attachments/716303341822672999/886051336519549019/no.jpg", "please stop spamming lol","spamming is sus. you're spamming. <:stevesmug:727202674587467857>", "i'm beginning to think y'all may have a problem","no wah. instead here's a turtle with a hat <:turtleyeehaw:873380927735205958>", f"y'all treat me like a wah machine but *i'm so much more, {message.author.mention}*", "go ask someone else for waluigi pics", "no.", "wah?"]
                    await message.channel.send(random.choice(responses))
                        
            if re.search('(?i)^wah.', message.content) and cooldown(message.author.id, 'wah', 15) and cooldown(message.guild.id, 'guild.wah', 60*60*24, write=False) == True:
                Waluigi = ['https://cdn.discordapp.com/attachments/668622610543935498/870716564779958352/paeewgo7i9u312.jpg', 'https://cdn.discordapp.com/attachments/716303341822672999/880179579044647002/waah.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179566738542652/waahh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179530482987068/waaaaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179525512728626/waa.png',
                        'https://cdn.discordapp.com/attachments/716303341822672999/880179527131750400/waaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179524086673448/wa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179522283114516/wahhhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179520253100093/wahhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179517681987594/wah.png', 'https://media.discordapp.net/attachments/683111565230342188/885962413457952768/image0.jpg','https://cdn.discordapp.com/attachments/716303341822672999/886000782997086249/w_a_a.png','https://media.discordapp.net/attachments/716303341822672999/886002244439380039/wa.webp','https://media.discordapp.net/attachments/534781603860316160/886044958547644466/unknown.png','https://media.discordapp.net/attachments/716303341822672999/886052239163129916/e07.png','https://media.discordapp.net/attachments/716303341822672999/886052462023299112/fxx8gwhs.png','https://cdn.discordapp.com/attachments/716303341822672999/886052535025160242/67c.png','https://cdn.discordapp.com/attachments/716303341822672999/886052735668084826/c2fy9ie1.png']
                await message.channel.send(random.choice(Waluigi))
        except:
            print(sys.exc_info())
       
    # @commands.Cog.listener()   
    # async def on_raw_reaction_add(self, payload):
    #     guild = self.bot.get_guild(payload.guild_id)
    #     channel = self.bot.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     # If reaction is :cramorantbruh: and message is in #dankmemes or my test channel
    #     if payload.channel_id == 881244618019205150 and payload.emoji.name == 'cramorantbruh' or payload.channel_id == 541085407039717386:
    #         reaction = discord.utils.find(lambda r: r.emoji.name == 'cramorantbruh', message.reactions)
    #         if reaction.count >= 8:
    #             if cooldown(guild.id, message.id, 604800*8, write=False):
    #                 await message.reply('Hello! For crimes against humanity, the court has found you https://c.tenor.com/x8Ao32hEVp8AAAAd/phoenix-wright-judge.gif')
    #                 try:
    #                     role = discord.utils.find(lambda r: r.id == 721839159299407924, guild.roles)
    #                     member = await guild.fetch_member(payload.user_id)
    #                     await member.add_roles(role)
    #                     await message.channel.send(f'You have been barred from {channel.mention}. Get out of my sight.')
    #                 except:
    #                     await message.channel.send("There's no punishment, but it's the thought that counts.")
    #                 cooldown(guild.id, message.id)
                
            
    @cog_ext.cog_subcommand(base="minecraft",
            name="say",
            description="Turns your text into Minecraft text",
            options=[
                create_option(
                    name="text",
                    description="What you'd like to say",
                    option_type=3,
                    required=True
                )
            ])
    async def minecraft_say(self, ctx: SlashContext, text):
        if len(text) <= 100:
            try:
                text_on_img(text=f"<{ctx.author.name}> {text}", size=32, color=(255,255,255))
                transparency()
                file = discord.File(fp="transparent_image_gen.png", filename=f"{ctx.author.name}_say.png")
                await ctx.send(file=file)
            except:
                embed = discord.Embed(title="Minecraft Say", description="❌ I think Steve must've died or something, sad", color=0xc84268)
                await ctx.send(embed=embed, hidden=True)
        else:
            embed = discord.Embed(title="Minecraft Say", description="❌ Please do not paste the entire Bee Movie script", color=0xc84268)
            await ctx.send(embed=embed, hidden=True)
        
def text_on_img(fp="image_gen.png", text="Hello", size=12, color=(255,255,0)):
	"Draw a text on an Image, saves it, show it"
	fnt = ImageFont.truetype('Minecraftia-Regular.ttf', size)
	# create image
	image = Image.new(mode = "RGB", size = (int(size/1.4)*len(text),size+30), color = "black")
	draw = ImageDraw.Draw(image)
	# draw text
	draw.text((10,10), text, font=fnt, fill=color)
    #  save it
	image.save(fp)
 
def transparency(fp="image_gen.png"):
    img = Image.open(fp)
    rgba = img.convert("RGBA")
    data = rgba.getdata()
  
    newData = []
    for item in data:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
            # storing a transparent value when we find a black colour
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)  # other colours remain unchanged
    
    rgba.putdata(newData)
    rgba.save("transparent_image_gen.png", "PNG")

def cooldown(user_id, command, cooldown = 5, write = True):
    # write = false lets us check if a cooldown has elapsed without resetting it
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                cooldowns = json.load(fp)
            time_diff = time.time() - cooldowns[user_id][f'{command}.cooldown']
            # user is in database for this command
            if time_diff >= cooldown:
                if write:
                    cooldowns[user_id][f'{command}.cooldown'] = time.time()
                    with open('users.json', 'w') as fp:
                        json.dump(cooldowns, fp, sort_keys=False, indent=4)
                return True
            else:
                return False
        except KeyError:
            # user isn't in database with this command
            with open('users.json', 'r') as fp:
                cooldowns = json.load(fp)
            try:
                cooldowns[user_id][f'{command}.cooldown'] = time.time()
            except KeyError:
                # user isn't in database at all
                cooldowns[user_id] = {}
                cooldowns[user_id][f'{command}.cooldown'] = time.time()
            finally:
                if write:
                    with open('users.json', 'w') as fp:
                        json.dump(cooldowns, fp, sort_keys=False, indent=4)
                return True
    else:
        # initialize database
        if write:
            cooldowns = {user_id: {}}
            cooldowns[user_id][f'{command}.cooldown'] = time.time()
            with open('users.json', 'w') as fp:
                json.dump(cooldowns, fp, sort_keys=False, indent=4)
        return True

def setup(bot):
    bot.add_cog(Fun(bot))
