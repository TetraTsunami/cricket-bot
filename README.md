# cricket-bot
Heya! This is a simple Discord bot written with [Pycord](https://github.com/Pycord-Development/pycord). I'm still learning to code, but I'd like to add many more functions soon!

### Commands
- A couple responses to common phrases in discord servers that I'm in
- Has a disproportionate number of pictures relating to Nintendo character Waluigi
- If people specifically spam "Wah" too much, it is disabled for the entire server for 24 hours.
![](https://media.discordapp.net/attachments/881244618019205150/925467914025443378/unknown.png)
![](https://media.discordapp.net/attachments/881244618019205150/925468423696314448/unknown.png)

Bot
- `/ping` Get the ping of the bot- useful for diagnosing issues.
- `/say` Allows the owner to make the bot say an arbitrary bit of text.

Minecraft
- `/minecraft ping` Get player count, icon, and motd (+online players/plugins!) of a Minecraft server using [mcstatus](https://github.com/Dinnerbone/mcstatus/)
![](https://media.discordapp.net/attachments/881244618019205150/925466923645435964/unknown.png)


Memegen
- `/memegen minecraft` Generates some funky text that looks like a chat message from Minecraft
![](https://media.discordapp.net/attachments/881244618019205150/925466446316855386/Jump_say.png)
- `/memegen generate` Generate a meme from one of many formats using the Imgflip API and a modified version of (pyimgflip)[https://github.com/TymanWasTaken/pyimgflip]
![](https://media.discordapp.net/attachments/881244618019205150/925467520566198322/unknown.png)
- `/memegen list` List avalible formats for use with `/memegen generate`
/
Discord
- `/discord user` Grab the avatar, ID, account creation date and server join date of another user or yourselfm
- `/discord emote` Grab the file and link to an emote
![](https://media.discordapp.net/attachments/881244618019205150/925467801957859389/unknown.png)
- `/discord actvity` Gives you a link to start a faaancy Activity in your voice channel! Requires permissions to create invites. Current activities are chess, offbrand amogus, and YouTube Together.

### Installation
...why would you want to do this?
I personally run Cricket in a Docker container, but she really only needs her requirements installed and an .env file in the same directory containing...
- `DISCORD_TOKEN` - discord bot token
- `SUPPORT_GUILD` - a guild for some commands related to the various cogs of the bot
- `IMGFLIP_USERNAME`/`IMGFLIP_PASSWORD` - login for an Imgflip account, used for some commands

If you'd like Cricket to generate text and disable the wah command when it's spammed, add any TTF font with the name `Minecraftia-Regular.ttf` in the directory before building.

If you want to run in Docker, pull the repo, create the .env, and run
`docker compose up -d --build` and you should be good.
