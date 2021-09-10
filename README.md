# cricket-bot
Heya! This is a simple canned response bot for Discord written in Python. I'm still learning to code, but I'd like to add many more functions soon!

### Commands
- A couple responses to common phrases in discord servers that I'm in
- If people specifically spam Wah too much, it gets disabled for the entire server for 24 hours. Was this worth the effort to make? Probably not.

Bot
- `/bot ping` Get the ping of the bot- useful for diagnosing issues.
- `/bot invite` Get an invite link for the bot.

Minecraft
- `/minecraft ping` Get player count, icon, and motd (+online players/plugins!) of a Minecraft server using [mcstatus](https://github.com/Dinnerbone/mcstatus/)

Discord
- `/discord user` Grab the avatar, ID, account creation date and server join date of another user or yourself TODO add persistence
- TODO `/discord emote` Grab the file of an emote, if possible?
- `/discord play` Gives you a link to start a faaancy Activity in your voice channel! Requires permissions to create invites. Current activities are chess, offbrand amogus, and YouTube Together.

### Screenshots
![](https://cdn.discordapp.com/attachments/716303341822672999/881648724013637752/unknown.png)
![](https://media.discordapp.net/attachments/716303341822672999/881649089698205736/unknown.png)

### Installation
...why would you want to do this?
I personally run Cricket in a Docker container, but she really only needs her requirements installed and a token in a .env file in the same directory like so:
![](https://media.discordapp.net/attachments/716303341822672999/881649790084063232/unknown.png?width=801&height=145)
If you'd like Cricket to generate text and disable the wah command when it's spammed, add any TTF font with the name `Minecraftia-Regular.ttf` in the directory before building.

If you want to run in Docker, pull the repo, create the .env, and run
`docker compose up -d --build` and you should be good.
