import asyncio
import sqlite3
from datetime import datetime, timedelta, timezone

import discord
from discord.commands import slash_command
from discord.ext import commands, tasks

from Utilities.format import command_embed
from Utilities.splatoon import get_next_splatfest
from cogs.utils.view import SplatfestRoleButton

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS splatfest_guilds (guild_id INTEGER, channel_id INTEGER, message_id INTEGER, role_id1 INTEGER, role_id2 INTEGER, role_id3 INTEGER, PRIMARY KEY(guild_id))")

COLOR_EMOJI = ( # these are the basic "squares" that discord uses for color emojis and their rgb values. using one of these is easier than using a custom emoji
    (221, 46, 68, "🟥"),
    (244, 144, 12, "🟧"),
    (253, 203, 88, "🟨"),
    (120, 177, 89, "🟩"),
    (85, 172, 238, "🟦"),
    (170, 142, 214, "🟪"),
    (192, 105, 79, "🟫"),
    (230, 231, 232, ":white_large_square:"), # because we hate consistency
    (49, 55, 61, ":black_large_square:"),
)

def hex_to_rgb(hex: int) -> tuple:
    return (hex >> 16) & 0xff, (hex >> 8) & 0xff, hex & 0xff

def nearest_color_hex(query: int):
    rgb = hex_to_rgb(query)
    return min( COLOR_EMOJI, key= lambda candidate: sum( (c - q) ** 2 for c, q in zip( candidate, rgb ) ))[3]

def nearest_color_rgb(query: tuple):
    return min( COLOR_EMOJI, key= lambda candidate: sum( (c - q) ** 2 for c, q in zip( candidate, query ) ))[3]

class Splatfest(commands.Cog):
    def __init__(self, bot:commands.Bot):
        loop = asyncio.get_event_loop()
        self.bot = bot
        self.lastUpdated = 0
        self.currSplatfest = loop.run_until_complete(self.batch_update())
        
    @tasks.loop(hours=1)
    async def batch_update(self):
        self.curr_splatfest = await get_next_splatfest()
        self.lastUpdated = datetime.now()
        print("Updated splatfest data")
        if self.curr_splatfest.endTime < datetime.now(timezone.utc) - timedelta(hours=12):
            await self.clean_up()
        
    @slash_command(description="Create a new Splatfest role selector.")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.has_permissions(manage_roles=True)
    async def splatfest(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)
        splatfest = self.curr_splatfest
        
        # See if we already have a message for this server
        update = False
        error = False
        if cur.execute(f"""SELECT * FROM splatfest_guilds WHERE guild_id = {ctx.guild.id}""").fetchone():
            try:
                update = cur.execute(f"""SELECT * FROM splatfest_guilds WHERE guild_id = {ctx.guild.id}""").fetchone()
                channel = self.bot.get_channel(update[1])
                if channel: await channel.get_partial_message(update[2]).delete()
            except:
                error = True
            
        # Make roles
        teamRoles = []
        if update:
            for existingRole in update[3:6]:
                role = ctx.guild.get_role(existingRole)
                if not role: await ctx.guild.create_role(name=f"Team {team.name}", color=team.color, mentionable=True)
                teamRoles.append(role)
        else:
            for team in reversed(splatfest.teams):
                topRole = ctx.guild.me.top_role.position
                role = await ctx.guild.create_role(name=f"Team {team.name}", color=team.color, mentionable=True)
                await role.edit(position=topRole)
                teamRoles.insert(0, role)
        
        view = discord.ui.View(timeout=None)
        for i, role in enumerate(teamRoles):
            view.add_item(SplatfestRoleButton(role, nearest_color_hex(splatfest.teams[i].color)))
                           
        embed = command_embed(ctx, title="Splatfest Terminal", body=f"""
                              Ding ding ding! We've got a new Splatfest coming up quick!
                              
                              **{splatfest.title}**
                              {splatfest.teams[0].name}, {splatfest.teams[1].name}, or {splatfest.teams[2].name}?
                              
                              Choose a side with the buttons below!
                              """, imageUrl=splatfest.artUrl).add_field(name="Starts", value=discord.utils.format_dt(splatfest.startTime)).add_field(name="Ends", value=discord.utils.format_dt(splatfest.endTime))
        
        message = await ctx.channel.send(embed=embed, view=view)
        
        # Update database
        if update:
            cur.execute(f"""UPDATE splatfest_guilds SET channel_id = {ctx.channel.id}, message_id = {message.id} WHERE guild_id = {ctx.guild.id}""")
        else:
            cur.execute(f"""
                INSERT INTO splatfest_guilds
                VALUES ({ctx.guild.id}, {ctx.channel.id}, {message.id}, {teamRoles[0].id}, {teamRoles[1].id}, {teamRoles[2].id})
                """)
        con.commit()
        # We have to send an ephemeral message to clear the ctx.defer() from earlier, since we didn't want to send the actual role selector as a reply.
        if error:
            await ctx.respond(embed=command_embed(ctx, title="Splatfest Role Selector", body="My records show that there's already a Splatfest role selector for this server, but I couldn't delete it. I made a new one in this channel- if you want to delete the old message, please do so manually."))
        if update:
            await ctx.respond(embed=command_embed(ctx, title="Splatfest Role Selector", body="There's already a Splatfest role selector for this server, so I moved it into this channel for you."), ephemeral=True)
        else:
            await ctx.respond(embed=command_embed(ctx, title="Splatfest Role Selector", body="I've created a Splatfest role selector, enjoy!"), ephemeral=True)
        
    @commands.Cog.listener()
    async def on_ready(self):
        """This function is called every time the bot restarts.
        If a view was already created before (with the same custom IDs for buttons)
        it will be loaded and the bot will start watching for button clicks again.
        """

        rows = cur.execute(f"""SELECT * FROM splatfest_guilds""").fetchall()
        for row in rows:
            # recreate the view 
            view = discord.ui.View(timeout=None)
            guild = self.bot.get_guild(row[0])
            for role_id in row[3:6]:
                role = guild.get_role(role_id)
                view.add_item(SplatfestRoleButton(role, nearest_color_hex(int(role.color))))

            # add the view to the bot so it will watch for button interactions
            self.bot.add_view(view)
        print("Reloaded preexisting Splatfest role selectors")

    @slash_command(description="Delete all Splatfest role selectors.")
    async def clean_up(self, ctx):
        await ctx.defer(ephemeral=True)
        rows = cur.execute(f"""SELECT * FROM splatfest_guilds""").fetchall()
        length =  len(rows)
        for row in rows:
            guild = self.bot.get_guild(row[0])
            for role_id in row[3:6]:
                try: role = guild.get_role(role_id)
                except: continue
                await role.delete()
            await guild.get_channel(row[1]).get_partial_message(row[2]).delete()
            cur.execute(f"""DELETE FROM splatfest_guilds WHERE guild_id = {guild.id}""")
            con.commit()
        await ctx.respond(embed=command_embed(ctx, title="Splatfest Role Selector", body=f"I've deleted {length} Splatfest role selectors for you."), ephemeral=True)
            
def setup(bot:commands.Bot):
    bot.add_cog(Splatfest(bot))
