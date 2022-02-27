# Update
It has been years now since I last did any work relating to my old chatbot projects, but seeing as they were some of my earliest experiences with programming (that I am actually somewhat proud of), I have decided to publicly archive the pieces of the code I could find. Due to me being a freshman in high school when a majority of the code was written, a lot of it was hardcoded and therefore likely doesnt work anymore. Additionally, I follow some poor programming practices as well. That being said, I also think this code shows some good examples of my problem solving skills though! The Serenebot project began as an IRC Bot that I wrote as a Twitch Chatbot for one of my Minecraft friends in 5th grade for her to use on her stream. I have long since lost that code, but I eventually set my sights on getting back into bot creation by making an interactive chatbot for my class's GroupMe chat in 7th grade. The API was less than well documented, and the code was full of global variables and personal information relating to my classmates (hence it not being archived publicly here). However, in making simple commands such as a weather command or a terminal I could control from the group chat, I learned a lot about different api's reading documentation, and other important things. I even wrote a watchdog script to send me logs when the bot crashed and to restart it so that I could minimize downtime when I was not home. 

This all culminated in my third project, a discord bot this time. Using what I learned from the watchdog script, I was able to remotely host the bot on a DigitalOcean droplet. It could play music, moderate users, create custom commands, take polls, get game stats, and countless other features all while being relatively easy to use! The bot code was also much more well organized. Unfortunately, I do not have the most recent version of the bot.py script available like I do with the toolbox.py, hence there are some utilities in the toolbox script that will seem out of place. All in all though, I just want to keep these memories here for the long haul.

The following was the original ReadMe from back when I was actively working on the bot:
---------------------------------------------------------------------------------------------


# Serenebot - Organic Homegrown Bot™
## Inspiration/Reason

Got a little bored over the summer when some people I played with asked me to get Discord. I then heard about all the different cool and interesting Discord bots that people had made, and decided to try and take a stab at making my own. It has also become a great way for me to interactively learn more about Python and API usage at the same time as being able to create something cool for my friends.

## Bot.py vs Toolbox.py

While I know that there are most likely much better ways of organizing the bot's code, this was the simplest thing I could think of at the time (it will most likely be changed later on to a more "correct" format).
Basically, Bot.py contains all the main event loops and commands, whereas Toolbox.py contains useful helper functions as well as all of the bot's "modules". The current list of modules is:
- Custom Commands (allows users to create their own simple commands)
- Polls (allows users to create and participate in their own polls)
- Jukebox BETA (allows users to control, request, and play music through one of the server's voice channels, currently a work-in-progress)

## Sources/Libraries Used

- The whole bot is written using the rewrite branch of Rapptz's wonderful [Discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) library. 
- The Jukebox module wouldn't have been possible either without rg3's [youtube-dl](https://github.com/rg3/youtube-dl) library.
- Also (as usual), I couldn't have gotten nearly this far without all the help I've received from [Stack Overflow](https://stackoverflow.com/).
