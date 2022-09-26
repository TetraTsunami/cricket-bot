
import sqlite3

import discord
from discord.ext import commands

con = sqlite3.connect("data.db")
cur = con.cursor()


class LinkButtons(discord.ui.View):
    def __init__(self, ctx: commands.Context, buttons: dict, timeout: int = None):
        """A View that displays buttons that link to a URLs.

        Usage (setting message is unneccessary if you don't want to disable the link):
            view = LinkButton(ctx, timeout=None, buttons={"Discord": "https://discord.com", "GitHub": "https://github.com"})
            message = await ctx.respond("This is a button!", view=view)
            view.message = message

        Args:
            ctx (commands.Context)
            buttons (dict): A dictionary of {label: url} to display as buttons.
            timeout (int): The amount of time to wait before disabling the buttons. Defaults to None.
        """
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.message: discord.Message = None
        for label in buttons:
            self.add_item(
                discord.ui.Button(
                    label=label, style=discord.ButtonStyle.link, url=buttons[label]
                )
            )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit_original_message(view=self)
        
class SplatfestRoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, emoji: discord.Emoji = None, exclusive: list = None):
        """
        A button for one role. A database connection is used to check which roles are mutually exclusive with this one.
        """
        super().__init__(
            label=role.name,
            emoji=emoji,
            style=discord.enums.ButtonStyle.secondary,
            custom_id=str(role.id),
        )

    async def callback(self, interaction: discord.Interaction):
        """This function will be called any time a user clicks on this button

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object that was created when the user clicked on the button
        """

        user = interaction.user
        actions = []
        # get the role this button is for (should be in the button id)
        role = interaction.guild.get_role(int(self.custom_id))

        if role is None:
            raise ValueError(f"Role with id {self.custom_id} not found")
        
        # Deal with exclusive roles
        # might look like (1023778645677981717, 1023778646760116335, 1023778647523479682)
        exclusiveRoleIDs = list(cur.execute(f"SELECT role_id1, role_id2, role_id3 FROM splatfest_guilds WHERE guild_id = {interaction.guild_id}").fetchone())
        # get rid of the role we want to give the user
        if role.id in exclusiveRoleIDs: exclusiveRoleIDs.remove(role.id)
        # get the roles we want to remove from the user
        invalidRoleIDs = filter(lambda r: r in exclusiveRoleIDs, [role.id for role in user.roles])
        if invalidRoleIDs: 
            for id in invalidRoleIDs:
                invalidRole = interaction.guild.get_role(id)
                await user.remove_roles(invalidRole)
                actions.append(f"Removed role {invalidRole.mention}")
        
        # add the role and send a response
        if role not in user.roles:
            # give the user the role if they don't already have it
            await user.add_roles(role)
            actions.append(f"Added role {role.mention}")
        else:
            # else, take the role from the user
            await user.remove_roles(role)
            actions.append(f"Removed role {role.mention}")
        await interaction.response.send_message(embed=discord.Embed(color=discord.Color.embed_background(), title="Splatfest Terminal", description='\n'.join(actions)).set_footer(text="Role Selector", icon_url=interaction.user.avatar.url), ephemeral=True)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit_original_message(view=self)
