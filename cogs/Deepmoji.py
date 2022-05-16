import logging
import os
import random

import discord
import requests
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv

from .utils.deepmoji import get_emoji
from .utils.embed import simple_embed

logger = logging.getLogger('discord')

load_dotenv()
if os.getenv('DEEPMOJI_URL'):
    deepmoji_url = os.getenv('DEEPMOJI_URL')
    if os.getenv('DEEPMOJI_FREQUENCY'): deepmoji_frequency = float(os.getenv('DEEPMOJI_FREQUENCY'))
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

class Deepmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command()
    async def deepmoji(
        self,
        ctx:discord.ApplicationContext, 
        sentence: str,
        hidden: Option(bool, 'Only shows results to you', required=False) = False):
        """Returns the top 10 emoji reactions for a given sentence"""
        try:
            emoji = get_emoji(sentence, deepmoji_url, min_prob=0, results=10)
            # print(f'got {emoji} for "{message.content}"')
            page = [f'*{sentence}*']
            for i in emoji:
                page.append(f'{i["emoji"]}: **{round(i["prob"]*100)}%**')
            await ctx.respond(embed=simple_embed(title="Deepmoji results",icon="😀", body='\n'.join(page), ctx=ctx), ephemeral=hidden)
                
        except requests.exceptions.HTTPError as e:
            await ctx.respond(embed=simple_embed(title="Deepmoji results",icon="Failure", body=f'Deepmoji error "{e}" on message "{ctx.message.content}"', ctx=ctx), ephemeral=True)
        
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if random.random() <= deepmoji_frequency:
                # 30% chance to trigger, but we have a high prob setting so it may not go off all that often
                    try:
                        emoji = get_emoji(message.content, deepmoji_url, 0.20)
                        if emoji:
                            await message.add_reaction(emoji[0]['emoji'])
                    except requests.exceptions.HTTPError as e:
                        logger.warning(f'Deepmoji error "{e}" on message "{message.content}"')
                        

def setup(bot):
    if deepmoji:
        bot.add_cog(Deepmoji(bot))
