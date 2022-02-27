##DO NOT FORGET TO SWITCH TO REWRITE BRANCH WHEN USING DISCORD.PY GITHUB!!!!!!!!
#TODO: BIGGEST CURRENT ISSUE WITH BOT: ROLE CHECKING IS SPECIFIC TO EACH SERVER AND THEREFORE HARD CODED FOR THE MAIN SERVER AS OF RIGHT NOW. THIS MUST BE FIXED FOR THE BOT TO JOIN MULTIPLE SERVERS EFFECTIVELY.
#TODO: FOR A SIMPLER, HALF DAY PROJECT, PROGRAM POLLING SYSTEM TO TAKE VOTES IN CHAT.
import discord
from toolbox import *
import aiohttp
import asyncio
#import atexit
import random

#EACH COMMAND MUST BE ADDED AS A KEY TO THIS DICTIONARY, AND ITS DESCRIPTION ADDED AS A VALUE. THIS DICTIONARY WILL BE USED TO GENERATE THE HELP EMBED.
commandDict = {'!help':'Gives a list of all commands and a short description of what each does and how to use them', '!greet <user>': 'Sends a friendly greeting to the user that you mention.', '!echo <text>': 'Makes the bot repeat whatever you told it to in the command.', '!owstats <platform> <battletag | gamertag | psn username> <mode>': 'Displays a few Overwatch stats for the given account (account type depends on which platform you specified in the command. The valid platforms are pc, xbl, and psn.), in either quick play or competitive mode (depends on which you sent with the command).', '!random <choices>':'Picks a random option out of the choices you give it (choices MUST be separated by a comma and a space). If you don\'t specify any choices, the bot will just pick a random person from the channel.', '!8ball <question>':'Gives you a definitive, totally legit answer to whatever yes-or-no question you specified in the command.', '!addcom <commandname> <commandoutput>':'Adds a custom command that outputs whatever you tell it.', '!delcom <commandname>': 'Deletes the specified custom command.', '!listcom': 'Shows a list of all current custom commands.' ,'!timeout <user> <optional time (in minutes)>': 'Prevents the mentioned user from talking in the chat for however many minutes you choose, if you don\'t specify an amount of minutes, it will default to 5 min.', '!kill <user>': 'Bans the user that was mentioned in the command. You must have the Ban Members permission in order to use this command.'}
magiclist = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it', 'As I see it, yes','Most likely','Outlook good','Yes','Signs point to yes','Reply hazy try again','Ask again later','Better not tell you now','Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']

#def cleanup():
    #print('saving')
    #customcommands(mode=)

#atexit.register(cleanup)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)#BE CAREFUL, RED LETTER B EMOJI BREAKS IDLE SHELL
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Game('Type \'!help\' for more info!'))
        #self.loop.create_task(self.welcome_msg())

    #TODO: FIX EMOJI COMMANDS, POSSIBLY WHILE LISTENING TO VSAUCE MUSIC
    # async def on_reaction_add(self, reaction, user):
    #     print('here1')
    #     if user != self.user and reaction.message.author != self.user:
    #         print(str(user.guild.roles))
    #         print(str(reaction.emoji))
    #         if (reaction.emoji == '⏲') and (user.roles[-1] >= user.guild.roles[-1]):
    #             print('here')
    #             timeoutcheck(reaction.message.author, mode=2, secs=30)
    #             await reaction.message.channel.send(reaction.message.author.display_name + ' has been silenced for 30 seconds.')

    async def on_message(self, message):
        try:
            if message.author != self.user:
                if timeoutcheck(message.author) is not True:
                    try:
                        #rolecheck(message, role=3, perm=['embed_links', 'attach_files'])
                        if messageparser(message, '!help') == -1:
                            async with message.channel.typing():
                                helpembed = discord.Embed(type='rich', title='Command List')
                                for key in commandDict.keys():
                                    helpembed.add_field(name=key, value=commandDict[key], inline=True)
                                helpembed.set_footer(text='Programmed with ♥ (lol) by Shane1470! Feel free to ask him if you have any questions!')
                            await message.channel.send(embed=helpembed)
                        elif messageparser(message, '!greet') is not False:
                            if len(message.mentions) != 1:
                                await message.channel.send('Hello!')
                            else:
                                await message.channel.send('Hi there, ' + message.mentions[0].display_name + '!')
                        elif messageparser(message, '!echo') is not False:
                            if messageparser(message, '!echo') == -1:
                                await message.channel.send('echo!')
                            else:
                                await message.channel.send(messageparser(message, '!echo')[0])
                        elif messageparser(message, '!owstats', argnum=3):
                            print('lol')
                            #TODO: POSSIBLY WORK ON SIMPLE FUNCTIONS (EX: MODS, BAN/KICK, etc.), ALLOW MODS TO TIMEOUT USERS BASED ON REACTION EMOTE, FIND WAY TO DYNAMICALLY GRAB AND ORDER ROLES.
                            statargs = messageparser(message, '!owstats', argnum=3)
                            #print(str(len(statargs)))
                            if statargs == -1 or len(statargs) != 3:
                                await message.channel.send('Sorry ' + message.author.display_name + ', but you must send the command followed by your platform, battletag/gamertag, and either quick play or competitive to receive stats. Ex: !owstats CoolSoldier#7612 competitive')
                                pass
                            else:
                                if statargs[0].lower().startswith('pc'):
                                    requesturl = 'https://owapi.net/api/v3/u/' + statargs[1].replace('#','-') + '/blob?platform=pc'
                                    reigon = 'us'
                                elif statargs[0].lower().startswith('p'):
                                    requesturl = 'https://owapi.net/api/v3/u/' + statargs[1] + '/blob?platform=psn'
                                    reigon = 'any'
                                elif statargs[0].lower().startswith('x'):
                                    requesturl = 'https://owapi.net/api/v3/u/' + statargs[1] + '/blob?platform=xbl'
                                    reigon = 'any'
                                else :
                                    await message.channel.send('Sorry ' + message.author.display_name + ', but you must list a valid platform before your battletag/gamertag. The valid platforms are pc, xbl, and psn.')
                                    pass

                                async with message.channel.typing():
                                    #TODO: FIX ISSUE WITH ARGUMENT PARSING THAT CAUSES ISSUES WHEN RECEIVING A CONSOLE USERNAME WITH SPACES IN IT
                                    async with aiohttp.ClientSession(headers={'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}) as session:
                                        async with session.get(requesturl, timeout=aiohttp.ClientTimeout(total=0, connect=None, sock_read=None)) as owstats:
                                            if owstats.status == 200:
                                                owjs = await owstats.json()
                                                #print(str(owjs))
                                                print('done')
                                                print(statargs[2])
                                                if statargs[2].lower().startswith('comp'):
                                                    if (owjs[reigon]['stats']['competitive'] is None) or (owjs[reigon]['heroes']['playtime']['competitive'] is None) or (owjs[reigon]['stats']['competitive']['overall_stats']['games'] < 10):
                                                        await message.channel.send('Sorry ' + message.author.display_name + ', but it appears that you have no (or incomplete) competitive stats on record. Please do your 10 placement matches, then close Overwatch to allow stats to update and try again.')
                                                        return
                                                    else:
                                                        topheroes = sorted(owjs[reigon]['heroes']['playtime']['competitive'], key=owjs[reigon]['heroes']['playtime']['competitive'].get, reverse=True)
                                                        owembed = discord.Embed(type='rich')
                                                        owembed.set_author(name='Overwatch Competitive Stats for ' + statargs[1], icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Overwatch_circle_logo.svg/600px-Overwatch_circle_logo.svg.png')
                                                        if owjs[reigon]['stats']['competitive']['overall_stats']['tier'] is None:
                                                            owembed.set_thumbnail(url=str(owjs[reigon]['stats']['competitive']['overall_stats']['avatar']))
                                                        else:
                                                            owembed.set_thumbnail(url=str(owjs[reigon]['stats']['competitive']['overall_stats']['tier_image']))
                                                            
                                                        if owjs[reigon]['stats']['competitive']['overall_stats']['comprank'] is None:
                                                            owembed.add_field(name='Current SR', value='Blizzard pls fix missing sr bug', inline=True)
                                                        else:
                                                            owembed.add_field(name='Current SR', value=str(owjs[reigon]['stats']['competitive']['overall_stats']['comprank']) + ' SR', inline=True)
                                                        owembed.add_field(name='Winrate', value=str(owjs[reigon]['stats']['competitive']['overall_stats']['win_rate']) + '%', inline=True)
                                                        owembed.add_field(name='Top 3 Heroes', value=str(topheroes[0]).title() + ', ' + str(topheroes[1]).title() + ', ' + str(topheroes[2]).title(), inline=True)
                                                        owembed.add_field(name='Win-Loss-Draw', value=str(owjs[reigon]['stats']['competitive']['overall_stats']['wins']) + '-' + str(owjs[reigon]['stats']['competitive']['overall_stats']['losses']) + '-' + str(owjs[reigon]['stats']['competitive']['overall_stats']['ties']), inline=True)
                                                        #owembed.set_footer(text='Overwatch Stats are grabbed from OWAPI. Check it out on Github at https://github.com/Fuyukai/OWAPI', icon_url='https://assets-cdn.github.com/images/modules/logos_page/Octocat.png')
                                                        await message.channel.send(embed=owembed)
                                                elif statargs[2].lower().startswith('q'):
                                                    topheroes = sorted(owjs[reigon]['heroes']['playtime']['quickplay'], key=owjs[reigon]['heroes']['playtime']['quickplay'].get, reverse=True)
                                                    owembed = discord.Embed(type='rich')
                                                    owembed.set_author(name='Overwatch Quick Play Stats for ' + statargs[1], icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Overwatch_circle_logo.svg/600px-Overwatch_circle_logo.svg.png')
                                                    owembed.set_thumbnail(url=str(owjs[reigon]['stats']['quickplay']['overall_stats']['avatar']))
                                                    owembed.add_field(name='Current Level', value=str(owjs[reigon]['stats']['quickplay']['overall_stats']['level'] + (owjs[reigon]['stats']['quickplay']['overall_stats']['prestige'] * 100)), inline=True)
                                                    owembed.add_field(name='Games Won', value=str(owjs[reigon]['stats']['quickplay']['overall_stats']['wins']), inline=True)
                                                    owembed.add_field(name='Time Played', value=str(int(owjs[reigon]['stats']['quickplay']['game_stats']['time_played'])) + ' Hours', inline=True)
                                                    owembed.add_field(name='Top 3 Heroes', value=str(topheroes[0]).title() + ', ' + str(topheroes[1]).title() + ', ' + str(topheroes[2]).title(), inline=True)
                                                    #owembed.set_footer(text='Overwatch Stats are grabbed from OWAPI. Check it out on Github at https://github.com/Fuyukai/OWAPI', icon_url='https://assets-cdn.github.com/images/modules/logos_page/Octocat.png')
                                                    await message.channel.send(embed=owembed)
                                                else :
                                                    await message.channel.send('Sorry ' + message.author.display_name + ', but your battletag/gamertag must be followed by either quick play or competitive (depending on which mode\'s stats you want.')
                                            else:
                                                owjs = await owstats.json()

                                                if owjs['msg'] == 'profile not found':
                                                    await message.channel.send('Sorry ' + message.author.display_name + ', but it appears you entered an invalid account.')
                                                elif owjs['msg'] == 'you are being ratelimited':
                                                    await message.channel.send('Sorry ' + message.author.display_name + ', but it appears the api is currently busy. Please wait a couple seconds and then try again.')
                                                print(str(owjs))
                        elif messageparser(message, '!timeout', argnum=2) and rolecheck(message, role=3):
                            arguments = messageparser(message, '!timeout', argnum=2)
                            if len(message.mentions) != 1 or message.mentions[0] == self.user:
                                await message.channel.send('Sorry ' + message.author.display_name + ', but you must mention one person to timeout.')
                            else:
                                if arguments[1] == '':
                                    timeoutcheck(message.mentions[0], mode=2, secs=300)
                                    await message.channel.send(message.mentions[0].display_name + ' has been silenced for 5 minute(s).')
                                else:
                                    if int(arguments[1]) > 30:
                                        await message.channel.send('Sorry ' + message.author.display_name + ', but you can\'t time someone out for longer than 30 minutes at a time.')
                                    else:
                                        timeoutcheck(message.mentions[0], mode=2, secs=(arguments[1]*60))
                                        await message.channel.send(message.mentions[0].display_name + ' has been silenced for ' + str(arguments[1]) + ' minute(s).')
                        elif messageparser(message, '!kill', argnum=1) and rolecheck(message,perm=['ban_members']):
                            if len(message.mentions) != 1 or message.mentions[0] == self.user :
                                await message.channel.send('Sorry ' + message.author.display_name + ', but you must specify a victim.')
                            else :
                                await message.mentions[0].ban()
                                await message.channel.send(message.mentions[0].display_name + ' has been slain. :crossed_swords: Goodbye...')

                        elif messageparser(message, '!addcom', argnum=2) and rolecheck(message, role=4):
                            custargs = messageparser(message, '!addcom', argnum=2)
                            if custargs == -1 or len(custargs) < 2:
                                await message.channel.send('Sorry ' + message.author.display_name + ', but you must specify the name of the new custom command followed by what it should output. Ex: !addcom test hello ')
                            else:
                                await message.channel.send(customcommands(mode=2, command=custargs[0], output=custargs[1], guild=message.guild))

                        elif messageparser(message, '!delcom', argnum=1) and rolecheck(message, role=4):
                            custargs = messageparser(message, '!delcom', argnum=1)
                            if custargs == -1:
                                await message.channel.send('Sorry ' + message.author.display_name + ', but you must specify the name of the custom command you would like to delete. Ex: !delcom test')
                            else:
                                await message.channel.send(customcommands(mode=3, command=custargs[0], guild=message.guild))

                        elif messageparser(message, '!listcom') == -1:
                            commandslist = customcommands(mode=4, guild=message.guild)
                            if len(commandslist) == 0:
                                await message.channel.send('It looks like there are currently no custom commands stored.')
                            else:
                                await message.channel.send('Here is a list of all current custom commands: $' + ', $'.join(commandslist))
                        elif message.content.startswith('!savecom') and message.author.id == HARDCODED_USER_ID_HERE :
                            customcommands(mode=5, guild=message.guild)
                            await message.channel.send('Commands successfully saved!')

                        elif messageparser(message, '!random') is not False:
                            if messageparser(message, '!random') == -1:
                                await message.channel.send('Alright, I\'ll just pick a random person from this chat! Thinking...')
                                async with message.channel.typing():
                                    await asyncio.sleep(3)
                                    await message.channel.send('And the lucky winner is: ' + random.choice(message.channel.members).display_name + '!')
                            else :
                                randomargs = messageparser(message, '!random')[0].split(sep=', ')
                                await message.channel.send('Hmm, let me think about it...')
                                async with message.channel.typing():
                                    await asyncio.sleep(3)
                                    await message.channel.send('The answer is: ' + random.choice(randomargs))
                        elif messageparser(message, '!8ball', failempty=True) or messageparser(message, '🎱', failempty=True):
                            await message.channel.send('Thinking...')
                            async with message.channel.typing():
                                await asyncio.sleep(3)
                                await message.channel.send('I say: ' + random.choice(magiclist))





                        #ELIF CHECKING FOR CUSTOM COMMAND MUST ALWAYS BE LAST!
                        elif message.content.startswith('$'):
                            await message.channel.send(customcommands(command=message.content.lstrip('$'), guild=message.guild))



                    except RoleError:
                        await message.channel.send('I\'m afraid I can\'t let you do that, ' + message.author.display_name + '.')
                else :
                    await message.delete()

            else:
                pass
        except Exception as e:
            print(e)
            if str(e) == '0, message=\'Attempt to decode JSON with unexpected mimetype: text/html; charset=utf-8\'':
                await message.channel.send('Sorry ' + message.author.display_name + ', please try using the command again.')
            else:
                await message.channel.send('Oops, it looks like something went wrong: ' + str(e) + '. Somebody go tell Shane lol.')


    #TODO: TURN THIS INTO A FUNCTION THAT CAN BE ADDED (AND CUSTOMIZED) AS A TASK TO THE LOOP THROUGH A CHAT COMMAND, ALLOWING FOR TIMED ANNOUNCEMENTS TO BE SET UP BY MODS!
    #async def welcome_msg(self):
       #for guild in self.guilds:
          #defaultChannel = discord.utils.find(lambda t: 'general' in t.name, guild.text_channels)
          #await defaultChannel.send("Hi, my name is " + self.user.name + '! Welcome to ' + guild.name + '!')


client = MyClient()
#DONT FORGET TO MAKE NEW BOT FOR TESTING, AS LIVE BOT IS CURRENTLY IN AN ACTUAL SERVER.
client.run(HARDCODED_API_KEY)
