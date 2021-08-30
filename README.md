# cricket-bot
Heya! This is a simple canned response bot for Discord written in Python. I'm still learning to code, but I'd like to add many more functions soon!

### Features
- A couple responses to common phrases in discord servers that I'm in
- Get player count, icon, and motd (+online players/plugins!) of a Minecraft server using [mcstatus](https://github.com/Dinnerbone/mcstatus:// "mcstatus")
- Slash commands! (currently just for the minecraft pinging command)

### Screenshots
![](https://cdn.discordapp.com/attachments/716303341822672999/881648724013637752/unknown.png)
![](https://media.discordapp.net/attachments/716303341822672999/881649089698205736/unknown.png)

### Installation
...why would you want to do this?
I personally run Cricket in a Docker container, but she really only needs her requirements installed and a token in a .env file in the same directory like so:
![](https://media.discordapp.net/attachments/716303341822672999/881649790084063232/unknown.png?width=801&height=145)

If you want to run in Docker, pull the repo, create the .env, and run
`docker compose up -d --build` and you should be good.

### Todo
- Proper config (ability to disable the fun commands if you're *lame*)
- Upgrade to the /minecraft ping command to make Cricket ping the server again every so often and update the message (persistence?)
- /discord emote to easily grab an emoji
- More fun commands, of course!
