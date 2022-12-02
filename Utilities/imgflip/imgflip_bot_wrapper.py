import json
import discord
from .imgflip import *


def chunks(lst, n):
    """https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
    Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# Create Imgflip instance
with open("configuration.json", "r") as config:
    data = json.load(config)
    imgflip = {
        "username": data["imgflip"]["username"],
        "password": data["imgflip"]["password"],
    }

api = Imgflip(username=imgflip["username"], password=imgflip["password"])
# Get list so we know if something is broken immediately
memes = api.get_memes()
memeNames = [e.name for e in memes]


def make_pages():
    page_list = []
    for idx, i in enumerate(chunks(memes, 10)):
        page_header = "These templates can be used in `/memegen generate`\n\n"
        page_contents = "\n".join(
            f"[{str(element.name)}]({str(element.url)}) ({element.box_count} boxes)"
            for element in i
        )
        page_list.append(
            discord.Embed(
                title=f"Meme Generator Page {idx+1}",
                description="".join([page_header, page_contents]),
                color=0xC84268,
            )
        )
    return {"meme_list": memes, "meme_names": memeNames, "paginator_list": page_list}
