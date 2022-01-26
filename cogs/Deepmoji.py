import os
import random
import requests

import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from dotenv import load_dotenv

from .utils.embed import simple_embed
from .utils.deepmoji import get_emoji

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
        sentence: str):
        try:
            emoji = get_emoji(sentence, deepmoji_url, min_prob=0, results=10)
            # print(f'got {emoji} for "{message.content}"')
            page = [f'*{sentence}*']
            for i in emoji:
                page.append(f'{i["emoji"]}: **{round(i["prob"]*100)}%**')
            await ctx.respond(embed=simple_embed(title="Deepmoji results",icon="😀", status='\n'.join(page)))
                
        except requests.exceptions.HTTPError as e:
            await ctx.respond(embed=simple_embed(title="Deepmoji results",icon="Failure", status=f'Deepmoji error "{e}" on message "{ctx.message.content}"'))
        
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if random.random() <= deepmoji_frequency:
                # 30% chance to trigger, but we have a high prob setting so it may not go off all that often
                    try:
                        emoji = get_emoji(message.content, deepmoji_url, 0.20)
                        # print(f'got {emoji} for "{message.content}"')
                        if emoji:
                            await message.add_reaction(emoji[0]['emoji'])
                    except requests.exceptions.HTTPError as e:
                        print(f'Deepmoji error "{e}" on message "{message.content}"')
                        

def setup(bot):
    bot.add_cog(Deepmoji(bot))
