import os
from dotenv import load_dotenv
import logging
import discord
import re
import time
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
intents = discord.Intents(messages=True, guilds=True)


@client.event
async def on_ready():
    print('*hacker voice* I\'m in. Started up as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
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

    if re.search('(?i).*cricket.*', message.content):
        await message.channel.send('i\'m literally right here wow')


logging.basicConfig(level=logging.WARNING)
client.run(TOKEN)
