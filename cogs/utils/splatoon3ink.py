

from datetime import datetime

import aiohttp
from dateutil import parser

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
                    splatfest.teams.append(SplatfestTeam(team["teamName"], color, team["id"]))

                return splatfest
            
# Debugging
if __name__ == "__main__":
    import asyncio
    import json

    loop = asyncio.get_event_loop()
    print(json.dumps(loop.run_until_complete(get_next_splatfest()).__dict__, indent=4))
