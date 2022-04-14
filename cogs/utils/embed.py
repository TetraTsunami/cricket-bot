import discord

def simple_embed(title='Command Embed' ,icon='None',status='None', ctx='None', command_name='command'):
    EMOJI_KEY = {
        'None':'',
        'Success':'✅',
        'Warning':'⚠️',
        'Failure':'❌',
        'YouTube':'<:youtubeicon:884155771556859984>',
        'Twitch':'<:twitchicon:887868334979317801>',
        'Discord':'<:discordicon:887868333716807680>',
        'Smash':'<:smashicon:895839672956239882>',
        'Minecraft':'<:GrassBlock:924075881562009640>'
              }
    if icon in EMOJI_KEY:
        emoji = EMOJI_KEY[icon]
    else: 
        emoji = icon
        
    STATUS_KEY = {
        'None':'',
        'idk':'❌ Something broke somewhere, try again later',
        'Permissions':'❌ I don\'t have permission to do that :(',
        'Length':'❌ Please don\'t paste the entire Bee Movie script, it\'s much too long',
        'NotFound':'❌ I couldn\'t find what you\'re looking for, sorry'
              }
    if status in STATUS_KEY:
        description = STATUS_KEY[status]
    else: 
        description = status
    embed = discord.Embed(title=f'{emoji} {title}', description=description, color=0xc84268)
    if ctx != 'None':
      embed.set_footer(text=f"/{command_name} | Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.display_avatar.url)
    return embed
    