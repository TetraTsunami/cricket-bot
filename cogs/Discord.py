import re

import discord
from cogs.utils.embed import command_embed
from cogs.utils.view import LinkButton
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands


def url(id, animated: bool = False):
    # Convert an emote ID to the image URL for that emote.
    extension = "gif" if animated else "png"
    return f"https://cdn.discordapp.com/emojis/{id}.{extension}"


class DiscordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    discord_utils = SlashCommandGroup("discord", "Commands related to Discord.")

    @discord_utils.command(description="Returns info about a user")
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def user(
        self,
        ctx: commands.Context,
        target: Option(str, "The user you would like to harass") = None,
        hidden: Option(
            bool, "Show results in an ephemeral message", required=False
        ) = False,
    ):
        # Use invoker if they didn't specify a target
        if not target:
            target = ctx.author.id
        user_id = re.sub("^<@|!|>$", "", str(target))
        # Now we have a user ID, let's get the user
        user = await self.bot.get_or_fetch_user(str(user_id))
        if not user:
            raise commands.CommandError(f"User {target} not found.")

        embed = (
            command_embed(
                ctx, title=f"{user.name}#{user.discriminator}", body=user.mention
            )
            .set_thumbnail(url=user.avatar.url)
            .add_field(name="ID", value=user.id, inline=False)
            .add_field(name="Created", value=discord.utils.format_dt(user.created_at))
        )
        if user.banner.url:
            embed.set_image(url=user.banner.url)
            view = LinkButton(ctx=ctx, buttons={"Download Avatar": user.avatar.url, "Download Banner": user.banner.url})
        else:
            view = LinkButton(ctx=ctx, buttons={"Download Avatar": user.avatar.url})
        member = ctx.guild.get_member(user.id)
        if member:
            embed.add_field(
                name="Joined", value=discord.utils.format_dt(member.joined_at)
            )
        await ctx.respond(embed=embed, view=view, ephemeral=hidden)
        
    @discord_utils.command(description="Returns info about this server")
    @commands.guild_only()
    async def server(self, ctx: commands.Context, hidden: Option(bool, "Show results in an ephemeral message", required=False) = False):
        embed = (
            command_embed(ctx, title=ctx.guild.name)
            .set_thumbnail(url=ctx.guild.icon.url)
            .add_field(name="ID", value=ctx.guild.id, inline=False)
            .add_field(name="Created", value=discord.utils.format_dt(ctx.guild.created_at), inline=False)
            .add_field(name="Members", value=ctx.guild.member_count)
            .add_field(name="Roles", value=len(ctx.guild.roles))
            .add_field(name="Channels", value=len(ctx.guild.channels))
        )
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner.url)
            view = LinkButton(ctx=ctx, buttons={"Download Icon": ctx.guild.icon.url, "Download Banner": ctx.guild.banner.url})
        else:
            view = LinkButton(ctx=ctx, buttons={"Download Icon": ctx.guild.icon.url})
        await ctx.respond(embed=embed, view=view, ephemeral=hidden)

    @discord_utils.command(description="Returns info about a custom emoji")
    async def emote(self, ctx, emoji: Option(str, "The emoji you'd like to download"), hidden: Option(bool, "Show results in an ephemeral message", required=False) = False):
        if not re.search("^<.?:.*:.*>$", emoji):
            return await ctx.respond(
                embed=command_embed(
                    "Emoji", "Failure", "That's not a custom emoji??", ctx=ctx
                ),
                ephemeral=True,
            )
        id = re.sub(r"^<.?:.*:|>$", "", emoji)
        name = re.sub(r"^<.?:|:.*>$", "", emoji)
        animated = False
        if re.search(r"^<a:", emoji):
            animated = True
        imageURL = url(id, animated)
        view = LinkButton(ctx=ctx, buttons={"Download Emoji": imageURL})
        embed = (
            command_embed(title="Emoji", imageUrl=imageURL, ctx=ctx)
            .add_field(name="Name", value=f"`{name}`")
            .add_field(name="Animated", value=animated)
            .add_field(name="ID", value=f"`{id}`")
        )
        await ctx.respond(embed=embed, view=view, ephemeral=hidden)


def setup(bot: commands.Bot):
    bot.add_cog(DiscordCog(bot))
