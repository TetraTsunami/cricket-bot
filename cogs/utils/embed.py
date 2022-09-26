import discord
from discord.ext import commands


def command_embed(
    ctx: discord.ApplicationContext,
    title="Command Embed",
    icon="",
    body="",
    imageUrl="",
    imageFile: discord.File = None,
):
    """Generates a simple embed with a title, icon, body, and image

    Args:
        ctx (discord.ApplicationContext): Ctx of the command, used to populate a rich footer.
        title (str, optional): Title of the embed. Defaults to 'Command Embed'.
        icon (str, optional): Emoji to place before the title. Defaults to no icon.
        body (str, optional): The body of the embed.
        imageUrl (str, optional): Image URL to place in the embed. Defaults to ''.
        imageFile (discord.File, optional): Image file to place in the embed. Defaults to 'None'.


    Returns:
        discord.Embed: Embed with the given parameters
    """

    embed = discord.Embed(color=0xC84268)
    if icon:
        embed.title = f"{icon} {title}"
    else:
        embed.title = title
    embed.description = body
    if imageUrl:
        embed.set_image(url=imageUrl)
    elif imageFile:
        embed.set_image(url=f"attachment://{imageFile.filename}")
    if ctx:
        embed.set_footer(
            text=f"/{ctx.command} | Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url=ctx.author.display_avatar.url,
        )
    return embed
