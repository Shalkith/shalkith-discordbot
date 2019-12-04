import random
import discord
from discord.utils import get
import time

from lookups import *
from skills import *
from hatching import *
from combat import *
#paste in discord token
#invite the bot
#type the below command in discord to roll 10 dice (d10s only for exalted)
#!roll 10



TOKEN = 'paste discord token here'
from creds import *
print (TOKEN)

client = discord.Client()
client.get_all_channels()


@client.event

async def on_message(message):
    print(message.content)
    formatting = '**'
    f = formatting

    user = message.author
    username = ''
    usernick = ''
    try:

        if message.author.nick == None:
            try:
                username = message.author.name
            except:
                pass
        else:
            try:
                usernick = message.author.nick
            except:
                pass
    except:
        pass
    if message.author.nick == None:
        usernick = username

    print(user)
    print(username)
    print(usernick)
    print(discord.member)
    if message.author == client.user:
        return
    if message.content.lower() == '!cleanup' and message.author.id == 272169658440744960:
        channel2 = client.get_channel(message.channel.id)
        async for x in channel2.history():
            await x.delete()


    elif 'i want to fight' in message.content.lower():

        changeneeded,bfname,role,bf = joinbattle(message)
        if changeneeded == True:
            print('author',message.author)
            #test = str(test)
            print('author2',test)
            await discord.Member.add_roles(message.author, role)
            await message.channel.send('added '+bf+' role to '+str(usernick)+' added to '+bfname)
        else:
            await message.channel.send(str(usernick)+", you're already in "+bfname)
    elif "i'm done fighting" in message.content.lower():
        changeneeded,role,bf,bfname = leavebattle(message)
        if changeneeded == False:
            await discord.Member.remove_roles(message.author, role)
            await message.channel.send('removed '+bf+' role from '+str(usernick)+' removed from '+bfname)
        else:
            await message.channel.send(str(usernick)+", you're not in a battlefield")
    else:
        pass

    print(message.content.lower().startswith('!combat'))
    if message.content.lower().startswith('!combat') and message.channel.id == 645819212241043516:
        print('testing')
        reply,status1,dragon1,status2,dragon2 = combatcommand(message)
        print(status1,dragon1,status2,dragon2)
        if status1 == 'starting':
            await message.channel.send(regainessence(dragon1,dragon2))
            #roll for random events
            time.sleep(.5)
            await message.channel.send(randomevents(dragon1))
            time.sleep(.5)
            await message.channel.send(randomevents(dragon2))
            time.sleep(.5)
            await message.channel.send('```Random Events is a work in progress and is not ready yet```')
            #roll for initative
            await message.channel.send(initative(dragon1,dragon2))


        else:
            await message.channel.send(reply)



    if message.content.lower().startswith('!hatch') and  message.channel.id == 646739468899844096:
        reply = starthatch(message)
        if 'A new Dragon has entered the world to compete for the title of Shalkith' in reply:
            from discord.utils import get
            role = get(message.guild.roles, name='Hatchling')
            await discord.Member.add_roles(message.author, role)



        await message.channel.send('```'+reply+'```')

    if message.content.lower().startswith('!mydragon'):
        text = mydragon(message.author.id)
        await message.author.send(text)
        #await client.send_message(user, text)


    if message.channel.id == 646739692795985950 and message.content.lower().startswith('!challenge ') and len(message.content.lower().split('!challenge ')[1])>1:
        text = message.content.lower().split('!challenge ')[1]
        text,did,challanger,defender,bf,bfname = newchallange(message.author.id,text)
        print('NEW BATTLEFIELD',bf)

        if bf != '-':
            from discord.utils import get
            role = get(message.guild.roles, name=bf)
            await discord.Member.add_roles(message.author, role)


        if did !='npc' and did != 'assign':
            await message.channel.send(text)


        else:
            print('sending start message')
            await message.channel.send(text)
            print('attempting to start an npc accept')
            text,did,challanger,defender,bf,bfname = newchallange(defender,challanger)
            await message.channel.send(text)

    if message.content.lower().startswith('!challange ') and '<@' in message.content and '>' in message.content:
        return
        text = message.content.split('!challange <@')[1]
        text = text.split('>')[0]
        challanger,defender = challange(message.author.id,text)
        if len(challanger) == 0:
            await message.channel.send('You have not hatched a dragon yet, <@%s>' % (message.author.id))
        elif len(defender) == 0:
            await message.channel.send('<@%s> has not hatched a dragon yet, <@%s>' % (text,message.author.id))
        else:
            await message.channel.send('<@%s> (%s) has challanged <@%s> (%s)!' % (message.author.id,challanger[1],text,defender[1]))



    if message.content.lower().startswith('!updatelatter'):
        from lookups import fixrank
        fixrank(True)
        data = dragonlatter()

        text = '```'

        l0 = 0
        l1 = 0
        l2 = 0
        l3 = 0
        l4 = 0

        for x in data:

            if len(x[0]) > l0:
                l0 = len(x[0])
            if len(x[1]) > l1:
                l1 = len(x[1])
            if len(x[2]) > l2:
                l2 = len(x[2])
            if len(x[3]) > l3:
                l3 = len(x[3])
            if len(x[4]) > l4:
                l4 = len(x[4])

        for x in data:
            if data.index(x) == 1:
                while len(x[0]) < l0:
                    x[0] = x[0] + '-'
                while len(x[1]) < l1:
                    x[1] = x[1] + '-'
                while len(x[2]) < l2:
                    x[2] = x[2] + '-'
                while len(x[3]) < l3:
                    x[3] = x[3] + '-'
                while len(x[4]) < l4:
                    x[4] = x[4] + '-'
            else:
                while len(x[0]) < l0:
                    x[0] = x[0] + ' '
                while len(x[1]) < l1:
                    x[1] = x[1] + ' '
                while len(x[2]) < l2:
                    x[2] = x[2] + ' '
                while len(x[3]) < l3:
                    x[3] = x[3] + ' '
                while len(x[4]) < l4:
                    x[4] = x[4] + ' '

        for x in data:
            if data.index(x) == 1:
                text = text +'---'+x[0]+'---'+x[1]+'---'+x[2]+'---'+x[3]+'---'+x[4]+'--\n'
            else:
                text = text +' | '+x[0]+' | '+x[1]+' | '+x[2]+' | '+x[3]+' | '+x[4]+' |\n'

        text = text + '```'
        channel2 = client.get_channel(648386904533762048)
        print(channel2.history())
        async for x in channel2.history():
            await x.delete()
        await channel2.send(text)
        #await message.channel.send(text)




client.run(TOKEN)
