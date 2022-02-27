#nickname checker, message argument parser etc.
#TODO: https://docs.python.org/3.5/library/configparser.html use this to set up permissions
import discord
import time
import asyncio
import pickle #Eventually figure out way to replace pickle with the safer JSON option.
import os
import sys
import configparser
import json
import youtube_dl

timeoutchair = {}
dirname = os.path.split(os.path.abspath(__file__))[0]
print(dirname)
customperms = {'CustomCommandAdd' : 'true', 'CustomCommandDelete' : 'false', 'ChangePFP' : 'false', 'ChangeNICK': 'false', 'votemanage':'false', 'musicmanage':'false'}
votedict = {}

with open(dirname + '/permissions.json', 'r') as config_file:
    custperms = json.load(config_file)
    config_file.close()

with open(dirname + '/customcommands', 'rb') as commfile:
    custcomms = pickle.load(commfile)
    commfile.close()

class RoleError(PermissionError):
    '''
    Raised when a user doesn't have the correct permissions/role in the channel to use a command.
    '''


def getbool(text):
    '''

    :param text: (str) The string equal to either 'true' or 'false' to be converted to bool.

    :return: (Bool) True or false.

    '''
    if text == 'true':
        return True
    elif text == 'false':
        return False
    elif text is False:
        return False
    elif text is True:
        return True




def messageparser(message, command, argnum=1, separator=' ', failempty=False, cleanmention=False):
    '''
    TODO: (TOO LAZY RN) ADD IN CHECK TO SEE IF AMOUNT OF ARGUMENTS IN LIST IS LESS THAN SPECIFIED IN ARGNUM PARAMETER, THIS CHECK MUST BE PLACED UNDER CHECK TO SEE IF LEN(ARGUMENTS) == 0.
    Function to pick arguments out of a command sent to the bot, also CHECKS PERMISSIONS/ROLE. REMEMBER THAT THE COMMAND ITSELF IS NOT INCLUDED IN THE FINAL LIST!

    :param message: (discord.Message) - The message to be parsed.

    :param command: (str) - The command (in lowercase) that the message should start with. If it is not found, the function will return false.

    :param argnum:(Optional int) - The number of arguments in the message. Defaults to one (1).

    :param separator: (Optional str) - The string used to separate arguments, defaults to a blank space (' ').

    :param failempty: (Optional bool) - If true, an empty argument list will return false rather than -1. Defaults to false.

    :param cleanmention: (Optional bool) - If true, it will replace mentions with the cleaned up text, rather than the ID (use only for echo type commands where you are mutating the string in some sort of way) (Defaults to false)

    :return: (List[]) - A list containing the arguments.
    '''
    if message.content.lower().startswith(command.lower()):
        if cleanmention is True:

            argstring = message.clean_content[len(command):].strip()
            splits = argnum - 1
            if separator == ' ':
                arguments = argstring.split(maxsplit=splits)
            else:
                arguments = argstring.split(separator, maxsplit=splits)
            if len(arguments) == 0:
                if failempty :
                    print('empty')
                    return False
                else:
                    return -1
            else:
                return arguments
        else:
            argstring = message.content[len(command):].strip()
            splits = argnum - 1
            if separator == ' ':
                arguments = argstring.split(maxsplit=splits)
            else:
                arguments = argstring.split(separator, maxsplit=splits)
            if len(arguments) == 0:
                if failempty:
                    print('empty')
                    return False
                else:
                    return -1
            else:
                return arguments
    else:
        return False

#TODO: POSSIBLY CUSTOM BOT PERMISSIONS (EX: ANNOUNCEMENTS, CUSTOM COMMANDS)
def rolecheck(message, mode=1, perm=None, rolemention=False):
    '''
    TODO: FIX ISSUE WHERE ROLES ARE SPECIFIC TO THE SERVER AND HARDCODED IN, CAUSING ERRORS WHEN ROLES ARE CHECKED BY LEVEL ON ANY OTHER SERVERS
    REMEMBER ROLE LIST STARTS WITH 0, THEN GOES FROM HIGH TO LOW
    :param message: (discord.Message) The message whose author needs a permission check.

    :param mode: (int) The mode the function should be using. 1 for checking permissions, 2 for adding custom permissions, 3 for deleting permissions, 4 for listing custom permissions. (Defaults to 1 for perm check)

    :param perm: (List[]) A list of permissions (as strings) that the user must have to use the command. You can see a list of the permission names at https://discordpy.readthedocs.io/en/rewrite/api.html?#discord.Permissions.create_instant_invite . Defaults to None.

    :param rolemention: (Optional bool) Whether or not the passed message mentions a role to be changed or only one user's permissions. Defaults to False for just one user.

    :return: (bool) True if user meets specified permission checks, otherwise it will raise a RoleError.
    '''

    if mode == 1:
        #print(custperms)
        if message.author.guild_permissions.administrator or message.author == message.guild.owner or message.author.id == HARDCODED_USER_ID_HERE :
            print('admin')
            return True
        # rolelist = list(message.guild.roles)
        # rolelist.append(rolelist.pop(0))
        # print(rolelist)

        #print(rolelist[role])
        else:
            discordperms = {}
            for n in iter(message.author.guild_permissions):
                discordperms[n[0]] = n[1]
            discordperms.update(custperms[str(message.guild.id)][str(message.author.id)])
            #print(discordperms)
            if all([getbool(discordperms[p]) for p in perm]):
                print('yes')
                return True
            else:
                print('no')
                raise RoleError

    if mode == 2:
        print('give perm')
        if perm[0] not in customperms:
            return 'Sorry, but that\'s not a valid custom permission.'
        else:
            if rolemention is True:
                role = message.role_mentions[0]
                for member in role.members:
                    custperms[str(message.guild.id)][str(member.id)][str(perm[0])] = 'true'
            else:
                member = message.mentions[0]
                custperms[str(message.guild.id)][str(member.id)][str(perm[0])] = 'true'
        with open(dirname + '/permissions.json', 'w') as config_file:
            json.dump(custperms, config_file)
            config_file.close()
            return 'Permissions changed successfully!'
    if mode == 3:
        print('take perm away')
        if perm[0] not in customperms:
            return 'Sorry, but that\'s not a valid custom permission.'
        else:
            if rolemention is True:
                role = message.role_mentions[0]
                for member in role.members:
                    custperms[str(message.guild.id)][str(member.id)][str(perm[0])] = 'false'

            else:
                member = message.mentions[0]
                custperms[str(message.guild.id)][str(member.id)][str(perm[0])] = 'false'

        with open(dirname + '/permissions.json', 'w') as config_file:
            json.dump(custperms, config_file)
            config_file.close()
            return 'Permissions changed successfully!'
    #REMEMBER, LISTING PERMS DOESN'T TAKE INTO ACCOUNT OWNERSHIP OR ADMIN PRIVILEGES
    if mode == 4:
        if rolemention is True:
            return 'Sorry, but you can only list custom permissions for one user at a time.'
        else:
            member = message.mentions[0]
            trueperms = {k:v for (k, v) in custperms[str(message.guild.id)][str(member.id)].items() if getbool(v) is True}
            return member.display_name + ' has access to the following bot permissions: ' + ', '.join(trueperms.keys())


#TODO: MAJOR ISSUE: FIX UNKNOWN PROBLEM THAT CAN CAUSE USERS TO HAVE INFINITE TIMEOUTS (OR TIME OUTS LONGER THAN SPECIFIED LENGTH)
def timeoutcheck(member, mode=1, **kwargs):
    '''

    TODO: FIX ISSUE WHERE TIMEOUT CURRENTLY CAUSES USERS TO BE SILENCED ON ALL SERVERS THAT THE BOT IS ON, NOT JUST THE ONE WHERE THE COMMAND WAS USED.
    :param member: (discord.Member) - The member to be timed out or checked for time out.

    :param mode: (Optional int) - The mode for the function. Mode 1 (default) checks if a user is currently timed out. Mode 2 adds a user to the timeout list.

    :param secs: (int) - The length of time (in seconds) that the timeout should last for.

    :return: True if user is timed out, false if not.
    '''
    if mode == 1:
        try:
            if (time.time() - timeoutchair[member.name][0]) < float(timeoutchair[member.name][1]):
                return True
            else :
                return False
        except KeyError:
            pass
    if mode == 2:
        timeoutchair[member.name] = [time.time(), kwargs['secs']]

#TODO: FIX ISSUE WITH ATTACHMENTS NOT BEING SAVED IN CUSTOM COMMANDS (GRAB ATTACHMENT URL, AND SAVE IT, MORE INFO AT https://discordpy.readthedocs.io/en/rewrite/api.html#discord.Attachment.url )
def customcommands(mode=1, **kwargs):
    '''

    :param mode: (Optional int) Tells what mode the function should use. 1 for using a custom command, 2 for adding/overwriting a custom command, 3 for deleting a custom command, 4 for listing all custom commands, 5 for saving all commands to json (on close). (Defaults to 1- Checking a command.)

    :param guild: (discord.Guild) The Guild that the command is being added to, deleted from, or used in. Allows for guild specific custom commands.

    :param command: (Optional str) The command name that will be added or checked to the commands list.

    :param output: (Optional str) The output of the new command.

    :return: (str) The output of the command that was used.
    '''
    #poor code, eventually replace with whatever collections.defaultdict is.
    if kwargs['guild'].id not in custcomms.keys():
        custcomms[kwargs['guild'].id] = {}
    if mode == 1:
        try :
            return custcomms[kwargs['guild'].id][kwargs['command']]
        except KeyError:
            return 'Sorry, but it looks like that custom command doesn\'t exist!'
    if mode == 2:
        if kwargs['command'].startswith('$'):
            return 'Sorry, but you can\'t start a new command name with \"$\". It confuzzles me way too much.'
        else:
            custcomms[kwargs['guild'].id][kwargs['command']] = kwargs['output']
            with open(dirname + '/customcommands', 'wb') as commfile:
                pickle.dump(custcomms, commfile)
                commfile.close()
            return 'Command $' + kwargs['command'] + ' was successfully added!'
    if mode == 3:
        try :
            del custcomms[kwargs['guild'].id][kwargs['command']]
            with open(dirname + '/customcommands', 'wb') as commfile:
                pickle.dump(custcomms, commfile)
                commfile.close()
            return 'Command $' + kwargs['command'] + ' was successfully deleted!'
        except KeyError:
            return 'Sorry, but it looks like that custom command doesn\'t exist!'
    if mode == 4:
        print(kwargs['guild'].id)
        print(custcomms)
        return list(custcomms[kwargs['guild'].id].keys())
    if mode == 5:
        with open(dirname + '/customcommands', 'wb') as commfile:
            pickle.dump(custcomms, commfile)
            commfile.close()
#TODO: POSSIBLY ADD SILENT/SECRET POLLS (MESSAGE USER SENDS TO VOTE IS DELETED AFTER SO THAT CHAT DOESNT KNOW WHO VOTED FOR WHAT), ADD POLL TIMERS
def vote(message, mode=1, override=False, **kwargs):
    '''

    :param message: (discord.Message) The message the command was sent with.

    :param mode: (int) The mode that the function should use. 1 to add/update a vote, 2 to start a poll, 3 to end a poll (automatically ends when all members have voted), and 4 to resend the poll embed. Defaults to 1.

    :param override: (bool) Defaults to False, if set to True, it will bypass the check of poll ownership before closing a poll.

    :param pollname: {REQUIRED str) The name of the poll to be created.

    :param polloptions: (Optional List[str]) A list of the choices for the new poll being created.

    :param votechoice: (Optional str) The option that the user is voting for.

    :return:
    '''
    if mode == 1:
        print(kwargs['votechoice'])
        print(votedict)
        if kwargs['votechoice'].lower() not in votedict[message.channel.id][kwargs['pollname']]['options']:
            return -1
        elif message.author.id in votedict[message.channel.id][kwargs['pollname']]['alreadyvoted']:
            return -2
        else:
            votedict[message.channel.id][kwargs['pollname']]['options'][kwargs['votechoice'].lower()] += 1
            votedict[message.channel.id][kwargs['pollname']]['alreadyvoted'].append(message.author.id)
            #all members have voted, poll automatically ends
            print(votedict)
            return votedict
    if mode == 2:
        try:
            #checks if a poll is already running in the channel
            if votedict[message.channel.id]:
                return -1
        except KeyError:
            votedict[message.channel.id] = {}
        #votedict[message.channel.id] = {}
        votedict[message.channel.id][kwargs['pollname']] = {}
        votedict[message.channel.id][kwargs['pollname']]['options'] = {}
        for opt in kwargs['polloptions']:
            votedict[message.channel.id][kwargs['pollname']]['options'][opt.lower()] = 0

        votedict[message.channel.id][kwargs['pollname']]['alreadyvoted'] = []
        votedict[message.channel.id][kwargs['pollname']]['creator'] = message.author
        print(votedict)
        return
    if mode == 3:
        if override is False:
            if message.author == votedict[message.channel.id][kwargs['pollname']]['creator']:
                finishkey = votedict[message.channel.id].pop(kwargs['pollname'])
                topopt = max(finishkey['options'], key=finishkey['options'].get)
                #check for tie
                tielist = [c for c, n in finishkey['options'].items() if n == finishkey['options'][topopt]]
                if len(tielist) > 1:
                    return {'top option' : tielist, 'numberofvotes' : finishkey['options'][topopt], 'tie': True}
                else:
                    return {'top option': topopt, 'numberofvotes' : finishkey['options'][topopt], 'tie':False}
            else:
                return -1
        else:
            finishkey = votedict[message.channel.id].pop(kwargs['pollname'])
            topopt = max(finishkey['options'], key=finishkey['options'].get)
            # check for tie
            tielist = [c for c, n in finishkey['options'].items() if n == finishkey['options'][topopt]]
            if len(tielist) > 1:
                return {'top option': tielist, 'numberofvotes': finishkey['options'][topopt], 'tie': True}
            else:
                return {'top option': topopt, 'numberofvotes': finishkey['options'][topopt], 'tie': False}

#ALLOW USERS TO SKIP SONGS THROUGH REACTIONS, ETC
#TODO: IMPORTANT: ADD ERROR HANDLERS FOR DIFFERENT SITUATIONS, EX: SKIPPING SONGS WITHOUT ANYTHING ELSE IN QUEUE, PAUSING OR PLAYING WHEN SONG IS ALREADY PAUSED OR PLAYING (OR WHEN NOTHING IS PLAYING), etc.
class Jukebox :
    def __init__(self, message, loop):
        #CHECK FOR VOICE CHANNEL CONTAINING USER WHO SENT MESSAGE, POSSIBLY STORE JUKEBOX INSTANCES IN GLOBAL DICTIONARY ON MAIN BOT.PY, AND REFERENCE BY GUILD ID TO CHECK IF GUILD ALREADY HAS AN INSTANCE OF JUKEBOX RUNNING
        #https://discordpy.readthedocs.io/en/rewrite/api.html#discord.Member.voice
        if message.author.voice is None:
            print('test')

            self.nochannel = True

        else :
            self.nochannel = False
            opts = {
                'format': 'webm[abr>0]/bestaudio/best',
                'prefer_ffmpeg': True
            }
            self.ffmpeg_options = {
                'before_options': '-nostdin',
                'options': '-vn'
            }
            self.ydl = youtube_dl.YoutubeDL(opts)
            self.voicechannel = message.author.voice.channel
            self.queue = []
            self.repeat = True
            self.needtorepeat = False
            self.repeatcounter = 0
            self.unplugging = False
            self.loop = loop


        pass

    async def insert_coin(self):
        self.voiceclient = await self.voicechannel.connect()

    async def addsong(self, message, song_link):
        #ADDS SONG TO QUEUE, ALONG WITH INFO ABOUT SONG (EX: NAME, USER WHO ADDED IT, WHAT SPOT IN QUEUE IT IS, ETC
        #POSSIBLY USE self.ydl.list_thumbnails() for Embed (if added)
        for song in self.queue:
            if song['url'] == song_link:
                await message.channel.send('Sorry ' + message.author.display_name + ', but that song is already in the queue!')
                return
        self.queue.append({'url': song_link, 'user': message.author, 'channel': message.channel, 'alreadyplayed': False, 'number': len(self.queue)})
        if not self.voiceclient.is_playing() and not self.voiceclient.is_paused():
            await self.nextSong(error='test')
        else:
            await message.channel.send('Your request has been added to the queue, ' + message.author.display_name + '!')
        pass

    async def play_song(self, song):


        # TODO: CREATE BACKEND FOR MUSIC PLAYER SYSTEM (PLAYLISTS, SKIPPING, SEARCHING, PAUSE/PLAY/VOLUME, CLEAN FORMATTING, etc.
        info = self.ydl.extract_info(song['url'], download=False)
        self.url = info['formats'][0]['url']
        self.title = info['title']
        await song['channel'].send('Now Playing: ' + self.title + ', suggested by ' + song['user'].display_name)
        player = discord.FFmpegPCMAudio(self.url, **self.ffmpeg_options)
        self.voiceclient.play(player, after=self.run_coro)
    def run_coro(self, error):
        coro = self.nextSong(error)
        fut = asyncio.run_coroutine_threadsafe(coro, self.loop)
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass

    async def nextSong(self, error):
        '''
        GRABS NEXT SONG FROM QUEUE AND CALLS PLAY_SONG WITH IT, REMOVES OLD SONG FROM QUEUE, ALSO CALLED IF SONG IS STOPPED/CANCELED
        :return:
        '''
        if self.unplugging:
            return
        if not self.repeat:
            try:
                self.nextinqueue = self.queue.pop(0)
                #print(self.queue)
                print(self.nextinqueue)
                await self.play_song(self.nextinqueue)
            except IndexError:
                print('out of songs')
                return
        else:
            try:
                for number, song in enumerate(self.queue):
                    if not song['alreadyplayed']:
                        self.queue[number]['alreadyplayed'] = True
                        self.needtorepeat = False
                        self.nextinqueue = song
                        await self.play_song(self.nextinqueue)
                        break
                    else:
                        self.needtorepeat = True
                if self.needtorepeat:
                    if self.repeatcounter >= len(self.queue):
                        self.repeatcounter = 0
                    for song in self.queue:
                        if song['number'] == self.repeatcounter:
                            self.nextinqueue = song
                            self.repeatcounter += 1
                            break
                    await self.play_song(self.nextinqueue)
            except:
                print('idk man')

            #     self.nextinqueue = self.queue.pop(0)
            #     #print(self.queue)
            #     print(self.nextinqueue)
            #     await self.play_song(self.nextinqueue)
            # except IndexError:
            #     print('out of songs')
            #     return


        pass

    async def removeSong(self, message):
        try:
            self.removedsong = self.queue.pop(self.nextinqueue)
            await message.channel.send(self.title + ' has been removed from the queue by ' + message.author.display_name + '!')
            await self.skipSong(message)
        except :
            await message.channel.send()



    async def skipSong(self, message):
        '''
        Call voiceclient.stop() to trigger nextSong, which will attempt to grab next song as well as increment queue

        ONE JUKEBOX INSTANCE PER GUILD
        :return:
        '''
        if self.voiceclient.is_playing():
            await message.channel.send(self.title + ' has been skipped by ' + message.author.display_name + '!')
            self.voiceclient.stop()
        else :
            await message.channel.send('Sorry ' + message.author.display_name + ', but you can\'t skip when nothing is playing!')
        pass

    async def pause(self):
        if (not self.voiceclient.is_paused()) and (self.voiceclient.is_playing()):
            self.voiceclient.pause()
        else:
            pass
        return

    async def resume(self):
        if self.voiceclient.is_paused():
            self.voiceclient.resume()
        else:
            pass
        return

    async def changeChannels(self, message):
        if message.author.voice is None:
            message.channel.send('Please join the voice channel that you would like the bot to move to, and then try again.')
            return -1
        else :

            await self.pause()
            await self.voiceclient.move_to(message.author.voice.channel)
            await self.resume()
        pass

    async def unplug(self):
        self.unplugging = True
        await self.voiceclient.disconnect()
        return












