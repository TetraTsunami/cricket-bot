import datetime
import json
import re
import os

import discord
import requests
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @cog_ext.cog_subcommand(base="discord",
            name="user",
            description="Returns info about a user (or yourself!)",
            options=[
                create_option(
                    name="user",
                    description="Name/ID of the user",
                    option_type=3,
                    required=False
                ),
                create_option(
                    name="hidden",
                    description="Only shows results to you",
                    option_type=5,
                    required=False
                )
            ])
    async def user_info(self, ctx: SlashContext, user=0, hidden=False):
        if user == 0:
            user = ctx.author_id
        target = await self.bot.fetch_user(re.sub(r'^<@!|>$', '', user))
        embed = discord.Embed(title=f'{target.name}#{target.discriminator}', description=target.mention, color=0xc84268)
        embed.set_thumbnail(url=target. avatar_url)
        embed.add_field(name="ID", value=target.id, inline=False)
        embed.add_field(name="Created", value=formatdate(target.created_at))
        try:
            guild = self.bot.get_guild(ctx.guild_id)
            member = await guild.fetch_member(target.id)
            embed.add_field(name="Joined", value=formatdate(member.joined_at))
        except:
            pass
        finally:
            await ctx.send(embed=embed,hidden=hidden)
    
    
    @cog_ext.cog_subcommand(base="discord",
            name="activity",
            description="Starts an activity in your current voice channel",
            options=[
                create_option(
                    name="activity",
                    description="ID of the activity (defaults to YouTube)",
                    option_type=3,
                    required=False,
                    choices=[
                        create_choice(
                            name="YouTube",
                            value="755600276941176913"
                        ),
                        create_choice(
                            name="Betrayal.io",
                            value="773336526917861400"
                        )
                    ]
                ),
                create_option(
                    name="hidden",
                    description="Only shows results to you",
                    option_type=5,
                    required=False
                )
            ])
    async def user_info(self, ctx: SlashContext, activity="755600276941176913", hidden=False):
        try: ctx.author.voice.channel 
        except: return await ctx.send('get in a voice channel, then we can talk', hidden=True)
        try:
            target = ctx.author.voice.channel
            r = requests.post(f"https://discord.com/api/v8/channels/{target.id}/invites", json = {
                    "max_age": 600,
                    "max_uses": 2,
                    "target_application_id": activity,
                    "target_type": 2,
                    "temporary": False}, headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"})
            invite = r.json()
            if r.status_code != 200:
                if activity == "755600276941176913": embed = discord.Embed(title="<:youtubeicon:884155771556859984> YouTube Activity", description="❌ I don't have permissions, oops!",color=0xc84268)
                else:
                    embed = discord.Embed(title="Discord Activity", description="❌ I don't have permissions, oops!", color=0xc84268)
                return await ctx.send(embed=embed,hidden=True)
            if activity == "755600276941176913": embed = discord.Embed(title="<:youtubeicon:884155771556859984> YouTube Activity", description=f"[Start a YouTube session in {ctx.author.voice.channel}](https://discord.gg/{r.json()['code']})",color=0xc84268)
            else:
                embed = discord.Embed(title="Discord Activity", description=f"[Start an Activity session in {ctx.author.voice.channel}](https://discord.gg/{r.json()['code']})", color=0xc84268)
            await ctx.send(embed=embed,hidden=hidden)
        except:
            if activity == "755600276941176913": embed = discord.Embed(title="<:youtubeicon:884155771556859984> YouTube Activity", description="❌ Couldn't make funny activity machine go brr, try again later",color=0xc84268)
            else:
                embed = discord.Embed(title="Discord Activity", description="❌ Couldn't make funny activity machine go brr, try again later", color=0xc84268)
            await ctx.send(embed=embed,hidden=True)
    # if (cmd === "yttogether") {
    #     const channel = message.mentions.channels.first() || message.guild.channels.cache.get(args[0]);
    #     if (!channel || channel.type !== "voice") return message.channel.send("❌ | Invalid channel specified!");
    #     if (!channel.permissionsFor(message.guild.me).has("CREATE_INSTANT_INVITE")) return message.channel.send("❌ | I need `CREATE_INSTANT_INVITE` permission");

    #     fetch(`https://discord.com/api/v8/channels/${channel.id}/invites`, {
    #         method: "POST",
    #         body: JSON.stringify({
    #             max_age: 86400,
    #             max_uses: 0,
    #             target_application_id: "755600276941176913", // youtube together
    #             target_type: 2,
    #             temporary: false,
    #             validate: null
    #         }),
    #         headers: {
    #             "Authorization": `Bot ${client.token}`,
    #             "Content-Type": "application/json"
    #         }
    #     })
    #         .then(res => res.json())
    #         .then(invite => {
    #             if (invite.error || !invite.code) return message.channel.send("❌ | Could not start **YouTube Together**!");
    #             message.channel.send(`✅ | Click here to start **YouTube Together** in ${channel.name}: <https://discord.gg/${invite.code}>`);
    #         })
    #         .catch(e => {
    #             message.channel.send("❌ | Could not start **YouTube Together**!");
    #         })
    # }
            
def formatdate(target: datetime.datetime):
    target = target.replace(tzinfo=datetime.timezone.utc)
    target_cst = target.astimezone(datetime.timezone(datetime.timedelta(hours=-6)))
    return target_cst.strftime("%A, %B %d, %Y %I:%M %p CST")

def setup(bot):
    bot.add_cog(Discord(bot))
