from datetime import datetime

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands

from .utils.embed import simple_embed

deleted_messages = {}
edited_messages = {'before':{},'after':{}}

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    snipe = SlashCommandGroup("snipe", "View a message before it was deleted or edited")
        
    @snipe.command(description="View recently deleted messages", default_permission=False) 
    @discord.ext.commands.is_owner()
    async def deleted(self, ctx):
        if ctx.guild.id not in deleted_messages:
            await ctx.respond(embed=simple_embed('View Deleted Messages','Discord','NotFound'),ephemeral=True)
            return
        cache = deleted_messages[ctx.guild.id] 
        page_contents = '\n\n'.join(f'{discord.utils.format_dt(time, style="R")} in {message.channel.mention} from {message.author.mention}:\n{message.clean_content}' for time, message in cache.items())
        await ctx.respond(embed=simple_embed('View Deleted Messages','Discord',page_contents, ctx=ctx),ephemeral=True)
        
    @snipe.command(description="View recently edited messages", default_permission=False) 
    @discord.ext.commands.is_owner()
    async def edits(self, ctx):
        if ctx.guild.id not in edited_messages['after']:
            await ctx.respond(embed=simple_embed('View Edited Messages','Discord','NotFound', ctx=ctx),ephemeral=True)
            return
        cache_before = edited_messages['before'][ctx.guild.id]
        cache_after = edited_messages['after'][ctx.guild.id] 
        page_contents = '\n\n'.join(f'{discord.utils.format_dt(time, style="R")} in {message.channel.mention} by {message.author.mention}:\n**FROM:** {cache_before[idx].content}\n**TO:** {message.clean_content}' for idx, (time, message) in enumerate(cache_after.items()))
        await ctx.respond(embed=simple_embed('View Edited Messages','Discord',page_contents, ctx=ctx),ephemeral=True)
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild.id
        if guild not in deleted_messages:
            deleted_messages[guild] = {}
        deleted_messages[guild][datetime.now()] = message
        if len(deleted_messages[guild]) > 8: deleted_messages[guild].pop(min(deleted_messages[guild]))
        
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild = after.guild.id
        if before.content == after.content or after.author.bot == True: return
        if guild not in edited_messages['after']:
            edited_messages['before'][guild] = []
            edited_messages['after'][guild] = {}
        edited_messages['before'][guild].append(before)
        edited_messages['after'][guild][datetime.now()] = after
        if len(edited_messages['before'][guild]) > 8: 
            edited_messages['before'][guild].pop(0)
            edited_messages['after'][guild].pop(min(edited_messages['after'][guild]))

def setup(bot):
    bot.add_cog(Snipe(bot))
