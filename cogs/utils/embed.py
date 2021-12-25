import discord

def simple_embed(title,icon='None',status='None'):
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
    emoji = EMOJI_KEY[icon]
    STATUS_KEY = {
        'None':'',
        'idk':'❌ Something broke somewhere, try again later',
        'Permissions':'❌ I don\'t have permission to do that :(',
        'Length':'❌Please don\'t paste the entire Bee Movie script, it\'s much too long'
              }
    if status in STATUS_KEY:
        description = STATUS_KEY[status]
    else: 
        description = status
    return discord.Embed(title=f'{emoji} {title}', description=description, color=0xc84268)
    