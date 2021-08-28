import os
from dotenv import load_dotenv
import logging
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import re
import time
import random
import asyncio
import sys
import socket
import io
import base64
from mcstatus import MinecraftServer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG_GUILD')

bot = commands.Bot("c!")
intents = discord.Intents(messages=True, guilds=True)
if DEBUG:
    slash = SlashCommand(bot, sync_commands=True, debug_guild=DEBUG)
else:
    slash = SlashCommand(bot, sync_commands=True)

wahcd = time.time()
cricketcd = wahcd
cricketcd2 = False


@bot.event
async def on_ready():
    print(f"*hacker voice* I\'m in. Started up as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    global wahcd
    global cricketcd
    global cricketcd2

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

    if re.search('(?i).*cricket.*', message.content) and cricketcd2 == True:
        cricketcd2 = False
        await message.channel.send(random.choice(['no, there\'s no help command. i\'m leaving.', 'yep, still here']))
    if re.search('(?i).*cricket.*', message.content) and cricketcd <= time.time():
        cricketcd = time.time() + 12*60*60
        cricketcd2 = True
        await message.channel.send('i\'m literally right here wow')

    if re.search('(?i)^wah.?', message.content) and wahcd <= time.time():
        wahcd = time.time() + 6*60*60
        Waluigi = ['https://cdn.discordapp.com/attachments/668622610543935498/870716564779958352/paeewgo7i9u312.jpg', 'https://cdn.discordapp.com/attachments/716303341822672999/880179579044647002/waah.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179566738542652/waahh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179530482987068/waaaaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179525512728626/waa.png',
                   'https://cdn.discordapp.com/attachments/716303341822672999/880179527131750400/waaa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179524086673448/wa.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179522283114516/wahhhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179520253100093/wahhh.png', 'https://cdn.discordapp.com/attachments/716303341822672999/880179517681987594/wah.png']
        await message.channel.send(random.choice(Waluigi))


@slash.subcommand(base="bot",
                  name="ping",
                  description="Returns info about the bot's ping")
async def bot_ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)} ms.")


@slash.subcommand(base="minecraft",
                  name="ping",
                  description="Returns info about a server",
                  options=[
                      create_option(
                          name="server",
                          description="Address of the server",
                          option_type=3,
                          required=True
                      )
                  ])
async def server_ping(ctx, server):
    await ctx.defer()
    try:
        target = MinecraftServer.lookup(server)
        status = target.status()

        embed = discord.Embed(title=server, color=0xc84268)
        embed.add_field(name="Version", value=status.version.name)
        embed.add_field(
            name="Players", value=f"{status.players.online}/{status.players.max}")
        embed.add_field(name="Ping", value=f"{round(status.latency)} ms")
        try:
            description = re.sub(r'^\s+|§.', '', status.description)
            description = re.sub(r'\n\s*', r'\n', description)
            embed.add_field(name="Description",
                            value=f"```{description}```", inline=False)
        except:
            pass
        try:
            query = target.query()
            embed.add_field(name="Online", value='\n'.join(query.players.names))
            embed.add_field(name="Plugins", value='\n'.join(query.software.plugins))
        except:
            pass
        # thumbnails are hard
        try:
            data = base64.b64decode(
                status.favicon.split(',', 1)[-1])
            file = discord.File(fp=io.BytesIO(data),filename="server_favicon.png")
            embed.set_thumbnail(url="attachment://server_favicon.png")
            await ctx.send(file=file, embed=embed)
        except:
            print(sys.exc_info())
            await ctx.send(embed=embed)
    except socket.timeout:
        embed = discord.Embed(
            title=server, description="timed out :(")
        await ctx.send(embed=embed)
        print(sys.exc_info())

    except:
        embed = discord.Embed(
            title=server, description="halp am havin a stronk")
        await ctx.send(embed=embed)
        print(sys.exc_info())


logging.basicConfig(level=logging.WARNING)
bot.run(TOKEN)
