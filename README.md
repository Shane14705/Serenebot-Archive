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
