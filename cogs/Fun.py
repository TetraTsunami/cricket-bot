import discord
from discord.ext import commands

import os
import re
import time
import random
import json
import asyncio

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

wahcd = time.time()
cricketcd = wahcd
cricketcd2 = False

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if re.search('(?i)^I\'m back*', message.content):
            await message.channel.send('hi back')

        if re.search('(?i)^Hi back*', message.content):
            await message.channel.send('i\'m the only one that gets to say that, clown')

        if re.search('(?i)^Hi the only one*', message.content):
            await message.channel.send('...')
            time.sleep(0.5)
            await message.channel.send('stop it')

        if re.search('(?i)^uwu', message.content):
            if random.choice([0, 0, 0, 1]):
                await message.channel.send('https://media.discordapp.net/attachments/716303341822672999/768908033609695234/dontdoituwu.png')
                time.sleep(0.5)
                await message.channel.send('yes, that\'s a threat')

        if re.search('(?i)(^d.?e.*d.?chat*|^chat d.?e.*d*|^d.e.a?.?d..?c.h.a.t*)', message.content):
            if (message.guild):
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

        if re.search('(?i).*cricket.*', message.content) and cooldown(message.author.id, 'cricket', 3600) == True:
            await message.channel.send('i\'m literally right here wow')

        if re.search('(?i)^wah.?', message.content) and cooldown(message.author.id, 'wah', 10) == True:
            wahcd = time.time() + 6*60*60
            Waluigi = ['https://cdn.discordapp.com/attachments/668622610543935498/870716564779958352/paeewgo7i9u312.jpg', 'https://cdn.discordapp.com/attachments/716303341822672999/880179579044647002/waah.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179566738542652/waahh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179530482987068/waaaaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179525512728626/waa.png',
                       'https://cdn.discordapp.com/attachments/716303341822672999/880179527131750400/waaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179524086673448/wa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179522283114516/wahhhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179520253100093/wahhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179517681987594/wah.png']
            await message.channel.send(random.choice(Waluigi))

def cooldown(user_id, command, cooldown):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        try:
            with open('users.json', 'r') as fp:
                cooldowns = json.load(fp)
            time_diff = time.time() - cooldowns[user_id][f'{command}.cooldown']
            # user is in database for this command
            if time_diff >= cooldown:
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
                with open('users.json', 'w') as fp:
                    json.dump(cooldowns, fp, sort_keys=False, indent=4)
                return True
    else:
        # initialize database
        cooldowns = {user_id: {}}
        cooldowns[user_id][f'{command}.cooldown'] = time.time()
        with open('users.json', 'w') as fp:
            json.dump(cooldowns, fp, sort_keys=False, indent=4)
        return True

def setup(bot):
    bot.add_cog(Fun(bot))