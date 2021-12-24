import discord

def simple_embed(title,state='None',description=''):
    STATES = {'Success':'✅',
              'Failure':'😳',
              'None':''
              }
    emoji = STATES[state]
    return discord.Embed(title=f'{emoji} {title}', description=description, color=0xc84268)
    