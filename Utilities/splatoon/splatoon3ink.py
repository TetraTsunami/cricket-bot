from datetime import datetime
import sqlite3

import aiohttp
from dateutil import parser

import discord

URL = "https://splatoon3.ink/data/festivals.json"


class SplatfestTeam:
    def __init__(self, name, color, id):
        self.id = id
        self.name = name
        self.color = color


class Splatfest:
    def __init__(
        self,
        id: str,
        region: str,
        title: str,
        startTime: datetime,
        endTime: datetime,
        artUrl: str,
        teams: list,
    ):
        self.id = id
        self.region = region
        self.title = title
        self.startTime = startTime
        self.endTime = endTime
        self.artUrl = artUrl
        self.teams = teams


def rgb_to_hex(rgb):
    return int("%02x%02x%02x" % rgb, 16)


async def get_next_splatfest() -> Splatfest:
    REGION = "US"
    splatfest = Splatfest("", "", 0, 0, "", "", [])
    async with aiohttp.ClientSession() as session:
        async with session.get(url=URL) as r:
            if r.status == 200:
                data = await r.json()
                target = data[REGION]["data"]["festRecords"]["nodes"][0]
                splatfest.id = target["id"]
                splatfest.region = REGION
                splatfest.startTime = parser.parse(target["startTime"])
                splatfest.endTime = parser.parse(target["endTime"])
                splatfest.title = target["title"]
                splatfest.artUrl = target["image"]["url"]

                for team in target["teams"]:
                    argbColor = team["color"]
                    color = rgb_to_hex(
                        (
                            int(argbColor["r"] * 255),
                            int(argbColor["g"] * 255),
                            int(argbColor["b"] * 255),
                        )
                    )
                    splatfest.teams.append(
                        SplatfestTeam(team["teamName"], color, team["id"])
                    )

                return splatfest


con = sqlite3.connect("data.db")
cur = con.cursor()


class SplatfestRoleButton(discord.ui.Button):
    def __init__(
        self, role: discord.Role, emoji: discord.Emoji = None, exclusive: list = None
    ):
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
        exclusiveRoleIDs = list(
            cur.execute(
                f"SELECT role_id1, role_id2, role_id3 FROM splatfest_guilds WHERE guild_id = {interaction.guild_id}"
            ).fetchone()
        )
        # get rid of the role we want to give the user
        if role.id in exclusiveRoleIDs:
            exclusiveRoleIDs.remove(role.id)
        # get the roles we want to remove from the user
        invalidRoleIDs = filter(
            lambda r: r in exclusiveRoleIDs, [role.id for role in user.roles]
        )
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
        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.embed_background(),
                title="Splatfest Terminal",
                description="\n".join(actions),
            ).set_footer(text="Role Selector", icon_url=interaction.user.avatar.url),
            ephemeral=True,
        )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit_original_message(view=self)
