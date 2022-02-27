'''
Created on Apr 23, 2016
Properties: t is equal to text of newest group message.
name is equal to str(Sender)
P:S: Remember to catch ZeroDivisionError, otherwise this will trigger a restart in watchdoge.

@author: Shane1470
For: Serenebot
'''
import configparser
import pickle
import random
import sys 
from time import strftime
import time

from groupy.object.responses import Group, Bot
from pushbullet import Pushbullet
import pywapi
import schedule
from wikipedia import wikipedia



global pollOpener
pollOpener = ''
global name1
name1 = ''
global opsListString
opsListString = []
global requester
requester = ''
global alreadyVoted
alreadyVoted = []
global maxVotes
maxVotes = 0
global votez
votez = ''
global pollOpen 
pollOpen = False
global tempCom
tempCom = ['nothing', 'here']
tempCom.clear()
global pickFile
pickFile = 'customcommands.p'
global custCommands
custCommands = {'test': 'test2'}
global pb
pb = Pushbullet(HARDCODED_API_KEY)
global p
p = 1
global opsString
opsString = ''
global opsList
opsList = []
global opsFile
opsFile = 'ops.p'
global custString
custString = ''
global custList
custList = []
global huskFile
huskFile = 'husky.p'
global huskies
huskies = []
global t
t = 'y'
global name
name = 'x'
global group
groups = Group.list().filter(name__contains='Testbot 2.0')
group = groups[0]
global serbot
serbot = Bot.list().first
global crasbot
crasbot = Bot.list().last
global requester
requester = ''
global oldt
oldt = 'z'
global b
b = 1
global restarters
restarters = ['Shane McKelvey', 'IFTTT via Shane McKelvey']
global answ
answ = ''
config = configparser.ConfigParser()
config.read('serenebot.ini')
SleepTimes = config['SleepTimes']
slowsleeptime1 = SleepTimes.get('sleepduringslowmode')
slowSleepTime = float(slowsleeptime1)
normleeptime1 = SleepTimes.get('sleepduringnormalmode')
normSleepTime = float(normleeptime1)
Versions = config['Versions']
version = Versions.get('version')
changeLoge = Versions.get('changelog')
hibernateTim = float(SleepTimes.get('sleepDuringHibernation'))



def newmessage(l):
    global group
    global t
    global name
    global oldt
    global messages
    global b
    global message
    if l == 1 :
        if b >= 130 :
            time.sleep(slowSleepTime)
            messages = 'x'
            message = 'y'
            print('Sleeping...')
            #oldt = 'I\'mma take a nap.'
            name = 'w'
            messages = group.messages()
            message = messages.newest
            name = message.name
            t = str(message.text)
           
        else :
            time.sleep(normSleepTime)
            messages = 'x'
            message = 'y'
            name = 'w'
            messages = group.messages()
            message = messages.newest
            name = message.name
            t = str(message.text)
            
    elif l == 2 :
        while p == 1:
            if t == 'Serenebot - Wake' and name in restarters :
                serbot.post('Good morning everybody!')
                break
            else:
                time.sleep(hibernateTim)
                messages = 'x'
                message = 'y'
                print('Hibernating...')
                # oldt = t
                name = 'w'
                messages = group.messages()
                message = messages.newest
                name = str(message.name)
                t = str(message.text)
                    
    elif l == 3 :
        t ='default'
        name = 'default'
            
        serbot.post('I\'m going down for some Maintenance, but I\'ll hopefully be back soon! See ya! -Serenebot ' )
        time.sleep(5)
        print('Cleared')
        sys.exit()

newmessage(1)
time.sleep(0.1)

def configure(op, con):
    config.read('serenebot.ini')
    if op == 'change' and con == 'sleep time - slow mode' :
        serbot.post('What would you like the settings value to be set to?')
        newmessage(1)
        time.sleep(0.1)
        while name != 'Shane McKelvey' :
            newmessage(1)
            time.sleep(0.3)
        config.set('SleepTimes', 'sleepduringslowmode', t)
        with open('serenebot.ini', 'w') as config_file :
            config.write(config_file)
        serbot.post('Ok Shane, Sleep time during slow mode has been set to ' + t + ' seconds! Restarting for changes to take effect!')
        raise ZeroDivisionError
    elif op == 'change' and con == 'sleep time - normal mode' :
        serbot.post('What would you like the settings value to be set to?')
        newmessage(1)
        time.sleep(0.1)
        while name != 'Shane McKelvey' :
            newmessage(1)
            time.sleep(0.3)
        config.set('SleepTimes', 'sleepduringnormalmode', t)
        with open('serenebot.ini', 'w') as config_file :
            config.write(config_file)
        serbot.post('Ok Shane, Sleep time during normal mode has been set to ' + t + ' seconds! Restarting for changes to take effect!')
        
        raise ZeroDivisionError
    elif op == 'change' and con == 'sleep time - hibernate' :
        serbot.post('What would you like the settings value to be set to?')
        newmessage(1)
        time.sleep(0.1)
        while name != 'Shane McKelvey' :
            newmessage(1)
            time.sleep(0.3)
        config.set('SleepTimes', 'sleepDuringHibernation', t)
        with open('serenebot.ini', 'w') as config_file :
            config.write(config_file)
        serbot.post('Ok Shane, Sleep time during hibernation has been set to ' + t + ' seconds! Restarting for changes to take effect!')
        
        raise ZeroDivisionError
    else :
        serbot.post('Invalid Settings option.')
        

def wildcard(x, y, e):
    global wild
    if e == 1 :
        wild = str(x[y:])
    elif e == 2 :
        wild = str(x[:-y])
    return(wild)


def pick(op, file, var):
    if op == 'dump' :
        m = open(file, 'wb+')
        pickle.dump(var, m)
        m.close()
    if op == 'load' :
        try :
            m = open(file, 'rb+')
            return(pickle.load(m))
        except :
            print('')      


def restart():
    raise ZeroDivisionError
    time.sleep(0.3)
    sys.exit()
    

def votes(options, op):
    global votez
    global opp
    global votess
    global name
    global alreadyVoted
    global maxVotes
    global pollOpen
    global pollOpener
    if op == 'open' :
        if pollOpen != True :
            opp = str.lower(options)
            votess = opp.split(',')
            votez = dict((k, 0) for k in votess)
            pollOpen = True
            pollOpener = name
            serbot.post('A new poll has begun! Do !poll vote <option> to vote!')
        else :
            serbot.post('There\'s still an open poll!')
    elif op == 'vote' :
        if str.lower(options) in votez :
            newmessage(1)
            votez[str.lower(options)] += 1
            serbot.post('Your vote has been added, ' + name + '!')
            alreadyVoted.append(name)
        else :
            serbot.post('The poll is a lie.')
    elif op == 'close' :
        if pollOpen != False and pollOpener == name :
            serbot.post('I\'m counting...')
            maxVotes = max(votez, key=votez.get)
            time.sleep(5)
            serbot.post('And the winner is: ' + str(max(votez, key=votez.get)) + ' with ' + str(votez[maxVotes]) + ' votes!')
            pollOpen = False
        else :
            serbot.post('You can\'t do that.')
    else :
        print('An error occured with the Vote Module : Invalid Op given.')

schedule.every().day.at('8:00') .do(restart)
schedule.every().day.at('20:00') .do(restart)       
       
def messagetv(op, push):
    if op == 'text' :
        pb.push_note('New Message!', push)
        serbot.post('Message sent!')
    elif op == 'video' :
        pass
    else :
        return()
    


def husky(op):
    global huskies
    global random_husky
    huskies = pick('load', huskFile, 'husky')
    if op == 'run' :
        random_husky = random.choice(huskies)
        serbot.post(random_husky)
    elif op == 'add' :
        newmessage(1)
        requester = name
        serbot.post('And what husky picture should I add?')
        newmessage(1)
        time.sleep(0.2)
        while name != requester :
            newmessage(1)
            time.sleep(0.2)
        if t in huskies :
            serbot.post('We already have that one.')
        else :
            huskies.append(t)
            time.sleep(0.1)
            pick('dump', huskFile, huskies)
        

def customcommands(com, op):
    global tempCom
    global requester
    global t
    global name
    global custCommands
    global custList
    global pick
    global custString
    custCommands = pick('load', pickFile, custCommands)
    if op == 'add' :
            if com not in custCommands.keys() :
                tempCom.append(str.lower(com))
                time.sleep(0.3)
                serbot.post('And what should the command say?')
                time.sleep(0.1)
                newmessage(1)
                while name != requester :
                    time.sleep(0.2)
                    newmessage(1)
                tempCom.append(newmessage(1))
                time.sleep(0.3)
                custCommands[tempCom[0]] = tempCom[1]
                time.sleep(0.5)
                tempCom = []
                pick('dump', pickFile, custCommands)
                serbot.post('The command was added successfully!')
            else :
                serbot.post('That command already exists.')
    elif op == 'run' :
        custCommands = pick('load', pickFile, custCommands)
        time.sleep(0.2)
        serbot.post(custCommands[com])
    elif op == 'delete' :
        if com in custCommands :
            del custCommands[str.lower(com)]
            serbot.post('Command Deleted successfully!')
            pick('dump', pickFile, custCommands)
        else :
            serbot.post('That\'s not a valid command.')
    elif op == 'list' :
        custCommands = pick('load', pickFile, custCommands)
        time.sleep(0.2)
        for key in custCommands :
            custList.append(key)
        custList.remove('hgbghtjkmvgyutctbdugjbtdth')
        custString = ','.join(custList)
        time.sleep(0.1)
        serbot.post('Current Commands: ' + custString)

        
def ops(na, op):
    global opsFile
    global opsList
    global opsString
    global opsListString
    opsList = pick('load', opsFile, opsList)
    name1 = na.replace('@', '')
    if op == 'add' :
        if name1 not in opsList :
            opsList.append(name1)
            pick('dump', opsFile, opsList)
            serbot.post(name1 + ' is now an op!')
        else :
            serbot.post(na + ' is already an op.')
    elif op == 'remove' :
        if name1 in opsList :
            opsList.remove(name1)
            pick('dump', opsFile, opsList)
            serbot.post(name1 + ' is not an op anymore.')
        else :
            serbot.post('That\'s not an op.')
    elif op == 'verify' :
        if name1 in opsList :
            return(True)
        else :
            return(False)
    elif op == 'list' :
        opsString = ','.join(opsList)
        serbot.post(opsString)
    else :
        print('')


def maths(prob):
    try :
        answ = str(eval(prob))
        return str(answ)
    except SyntaxError :
        serbot.post('Sorry, I couldn\'t understand that problem. Try being more specific.')
    except ZeroDivisionError :
        serbot.post('Don\'t divide by zero!')

    
def weather(zipc, op):
    weather_com_result = pywapi.get_weather_from_weather_com(zipc, 'imperial')
    if op == 'today' :
        serbot.post("The Weather Channel says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "°F now with a high of " + weather_com_result['forecasts'][0]['high'] + '°F and a ' + weather_com_result['forecasts'][0]['day']['chance_precip'] + '% chance of rain in ' + zipc + '.')
    elif op == 'tomorrow' :
        serbot.post('The Weather Channel says: Tomorrow will be ' + weather_com_result['forecasts'][1]['day']['text'].lower() + ' with a high of ' + weather_com_result['forecasts'][1]['high'] + '°F and a ' + weather_com_result['forecasts'][1]['day']['chance_precip'] + '% chance of rain!')
        
        
def wiki(ques):
    try :
        serbot.post(str(wikipedia.summary(str(ques)), sentences=1, auto_suggest=True))
    except :
        serbot.post('Sorry, I couldn\'t find that.')
        raise ZeroDivisionError
    
    
def helper(op) :
    if 'isop' in op :
        serbot.post('Do !isop <@username> to see if said username is an op!')
    elif 'custom' in op :
        if ops(name, 'verify') :
            serbot.post('To add a command do #addcom <command> . To delete a command do #delcom <command> . To list all available custom commands do #listcom . To run one of these commands, put a \'#\' in front of it so you get #<command>.')
        else :    
            serbot.post('To list all available custom commands do #listcom . To run one of these commands, put a \'#\' in front of it so you get #<command>.')
    elif 'weather' in op :
        serbot.post('To get the weather do !weather <zipcode> <today or tomorrow> . Depending on whether you put today or tomorrow it\'ll show you a different weather forecast.')        
    elif 'wikipedia' in op :
        serbot.post('WARNING: This module does not always work and is very specific. Doing !wikipedia <nameofawikipediapage> will (if the bot can find it) give you a summary of said wikipedia page.')    
    elif 'math' in op :
        serbot.post('This module works using python\'s math syntax, basically meaning 6 divided by 3 == 6 / 3 . 6 times 3 == 6 * 3 . 6 to the third power == 6 ** 3 . To run the command, do !math <mathproblem> .')
    elif 'husky' in op :
        if ops(name, 'verify') :
            serbot.post('Do !husky add to add a picture to the !husky command. Run !husky to get a random picture of a husky.')
        else :
            serbot.post('Do !husky to get a random picture of a husky.')
    elif 'tim' in op :
        serbot.post('Do !tim to get the current time!')
    elif 'vote' in str(op) :
        if ops(name, 'verify'):
            serbot.post('Do !poll open <option1>,<option2>,<option3> to open a new poll. Do !poll vote <option> to vote in a poll. Do !poll close to close a poll.')
        else :
            serbot.post('Do !poll vote <option> to vote for said option in a poll!')
    elif op == '' :
        serbot.post('To get help with a specific module, do !help <module> . Installed Modules: Custom Commands, Weather, Wikipedia, math, husky, tim, vote, isop.') 
    else :
        serbot.post('That\'s not a valid help command.')
        
            
def replies():
    global oldt
    global p
    global b
    global restarters
    global requester
    p = 1
    while p == 1 :  
        newmessage(1)
        schedule.run_pending()
        b += 1
        if b == 130 :
            print('Going to Sleep...')
        else :
            
            while  t != oldt :
                
                newmessage(1)
                if str.lower(t).startswith(str.lower('!help')) :
                    helper(str(wildcard(t, 6, 1)))
                    b = 1
                    oldt = t 
                    newmessage(1)
                    break
                
                elif str.lower(t) == 'hi serenebot' :
                    serbot.post('Hi there ' + name + ', I\'m Serenebot! Nice to meet you! I\'m this chat\'s personal bot!')
                    b = 1
                    oldt = t 
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!settings')) and name == 'Shane McKelvey' :
                    configure('change', str.lower((wildcard(t, 10, 1))))
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == 'sweet caroline' :
                    serbot.post('Oh, Oh ,Oh, Good tims never seemed so good!')
                    b = 1
                    oldt = t                                     
                    newmessage(1)
                    break
                
        
                elif 'who\'s crashbot' in str.lower(t) :
                    crasbot.post('Oh, me? My name\'s Crashbot! As you may know, my sister Serenebot crashes a lot. I\'m here to make sure she gets back up after crashing!')
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith('can we dig it') :
                    serbot.post('We can dig it!')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif 'is it lit' in str.lower(t) :
                    serbot.post('Why yes. Yes it is.')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
    
                
                elif str.lower(t) == 'hello world!' :
                    serbot.post('World says Hello!')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                
                elif str.lower(t) == 'who\'s serenebot' :
                    serbot.post('Hi there! I\'m a chat bot written in Python for GroupMe! I was programmed by Shane, so if you have any questions, ask him.')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif 'how\'s the bird doing' in str.lower(t) :
                    serbot.post('https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/KFC_logo.svg/1024px-KFC_logo.svg.png')
                    oldt = t     
                    b = 1
                    newmessage(1)  
                    break
                
            
                elif str.lower(t) == '!version' :    
                    serbot.post('Thank you for choosing ' + version + ' as your GroupMe chatbot!') 
                    oldt = t
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == '!changelog' :
                    serbot.post(changeLoge) 
                    oldt = t
                    b = 1
                    newmessage(1)
                    break
                
             
                elif str.lower(t) == 'wake up, stupid' :
                    serbot.post(strftime('But it\'s %I:%M %p ! That\'s like, midnight!'))
                    oldt = t     
                    b = 1    
                    newmessage(1)  
                    break
                
                
                elif str.lower(t) == '!husky' :
                    husky('run')
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == '!husky add' and ops(name, 'verify') :
                    husky('add')
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == '!song' :
                    serbot.post('Seeing as this is the first real \'STABLE\' release, I figured this song would make sense. You can check it out at: http://apple.co/28V3jFj (iOS) http://bit.ly/28SIydE (Android)')
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == '!tim' :
                    serbot.post(strftime('It\'s %I:%M %p'))
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == 'alexander hamilton' :
                    serbot.post('I\'m just like my country, I\'m young, scrappy, and hungry and I\'m not throwing away my shot!')
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == '!credits' :
                    serbot.post('First of all, this bot wouldn\'t be possible without the \'wonderful\' people over at Testbot. Second of all, I would like to think anybody who ever said \'Wow, that\'s a really cool robot\'. Because I spent 2 months on it. - Shane')
                    oldt = t  
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!weather')) :
                    if 'today' in t :
                        zipcc = wildcard(t, 9, 1)
                        zipco = wildcard(zipcc, 6, 2)
                        weather(zipco, wildcard(t, 15, 1))
                    elif 'tomorrow' in t :
                        zipcc = wildcard(t, 9, 1)
                        zipco = wildcard(zipcc, 9, 2)
                        weather(zipco, wildcard(t, 15, 1))
                    else :
                        serbot.post('I can\'t figure that out...')    
                    oldt = t 
                    b = 1
                    newmessage(1)    
                    break
                
                elif name in restarters and str.lower(t) == 'serenebot - restart' :
                    restart()
                    oldt = t 
                    time.sleep(1)
                    b = 1
                    newmessage(1)
                    break
                
                elif str(name) in restarters and str.lower(t) == 'serenebot - sleep' :
                    serbot.post('Imma take a SUPER-NAP!!')
                    b = 1
                    oldt = t     
                    newmessage(2)
                    break
                
                elif str(name) == 'Shane McKelvey' and str.lower(t) == 'Serenebot - Off' :
                    oldt = t 
                    b = 1
                    newmessage(3)
                    break
                
                elif str(name) == 'Shane McKelvey' and str.lower(t) == '!crash' :
                    raise TypeError
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif 'you can\'t always get what you want' in str.lower(t) :
                    serbot.post('Ohh, but if you try sometims, you just might find, you get wat you neeeeed!')
                    oldt = t
                    b = 1
                    newmessage(1)
                    break
                
                
                elif 'time' in str.lower(t) and name != 'Serenebot' :
                    serbot.post('Did you mean tim? (I\'ll bet you did)')
                    oldt = t
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t) == 'i hate dogs' :
                    serbot.post('How dare you say such things ' + name + '!')
                    oldt = t
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!wikipedia')) :
                    wiki(wildcard(t, 11, 1))
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!math')) :
                    try :
                        serbot.post('The answer is ' + maths(wildcard(t, 6, 1)) + '!')
                    except TypeError :
                        print('')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!op add')) and name == 'Shane McKelvey' :
                    ops(wildcard(t, 8, 1), 'add')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!op remove')) and name == 'Shane McKelvey' :
                    ops(wildcard(t, 11, 1), 'remove')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!op list')) :
                    ops(wildcard(t, 9, 1), 'list')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!isop')) :
                    opCheck = wildcard(t, 6, 1).replace('@', '')
                    if ops(opCheck, 'verify') :
                        serbot.post(opCheck + ' is an op. You should trust them!')
                    else :
                        serbot.post(opCheck +  ' is not an op.')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!poll open')) :
                    if ops(name, 'verify') :
                        votes(wildcard(t, 10, 1), 'open')
                    else :
                        serbot.post(name + ' does not simply take a poll.')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('#')) :
                    global custCommands
                    if 'addcom' in wildcard(t, 1, 1) :
                        if ops(name, 'verify') :        
                            requester = name
                            customcommands(wildcard(t, 8, 1), 'add')
                            b = 1
                        else :
                            serbot.post('What do you think you\'re doing, ' + name + '?')
                    elif 'listcom' in wildcard(t, 1, 1) :
                        requester = name
                        customcommands(wildcard(t, 8, 1), 'list')
                        b = 1
                    elif str.lower(wildcard(t, 1, 1)) in custCommands :
                        customcommands(str.lower(wildcard(t, 1, 1)), 'run')
                        b = 1
                    elif 'delcom' in wildcard(t, 1, 1) :
                        if ops(name, 'verify') :
                            customcommands(wildcard(t, 8, 1), 'delete')
                        else :
                            serbot.post('Hey, ' + name + ' stop pushing my buttons!')
                        b = 1
                    else :
                        print('')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!poll vote')) :
                    if name not in alreadyVoted :
                        votes(wildcard(t, 10, 1), 'vote')
                        b = 1
                    else :
                        print('2')
                        serbot.post('You already voted, ' + name + '.')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                 
                elif str.lower(t).startswith(str.lower('!poll close')) :
                    if ops(name, 'verify') :
                        votes('nothing here', 'close')
                    else :
                        serbot.post('You will not close our democracy!')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('!messagetv')) and name == 'Shane McKelvey' :
                    messagetv('text', str(wildcard(t, 11, 1)))
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                elif str.lower(t).startswith(str.lower('it\'s something unpredictable')) :
                    serbot.post('But in the end it\'s right! I hope you had the tim of your life!')
                    oldt = t 
                    b = 1
                    newmessage(1)
                    break
                
                else :
                    oldt = t
                    b += 1
                    newmessage(1)
                    break    
                