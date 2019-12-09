def attackcheck(d1,d2):
    import creds
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select name from combattable where rank = 'attacking' and (name ='%s' or name ='%s')" % (d1,d2))
    query2 = ("select name from combattable where rank = 'waiting to attack' and (name ='%s' or name ='%s')" % (d1,d2))

    data = []
    cursor.execute(query)

    for x in cursor:
        data.append(x[0])
    cursor.execute(query2)
    for x in cursor:
        data.append(x[0])

    print(data)


def movedragon(owner,dragon,rangespace):

    downer,dname,dtext,davailablemoves = movecheck(dragon,'-123')
    if davailablemoves == '-':
        return "It's not time to move right now\nType !combat start to see the current status",'-','-'


    if rangespace in davailablemoves:
        import creds
        import mysql.connector
        u = creds.mysqlun # MySQL username
        p = creds.mysqlpw # MySQL password
        h = creds.mysqlhost # MySQL server
        db = 'shalkith' # MySQL datanase name
        cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
        cursor = cnx.cursor(buffered=True)
        query = ("select rank,combatstatus from combattable where name = '%s'" % (dragon))

        data = []
        cursor.execute(query)

        for x in cursor:
            data.append(x)
        status = data[0][0]
        dragon2= data[0][1]

        query = ("select rank,name,owner from combattable where name = '%s'" % (dragon2))
        data = []
        cursor.execute(query)

        for x in cursor:
            data.append(x)
        d2status = data[0][0]
        d2dragon2= data[0][1]
        d2owner = data[0][2]



        if status == 'waiting to move':
            return "It's not your turn to move yet",dragon2,d2owner
        elif status == 'moving' and d2status == 'waiting to move':
            query = "update combattable set rank = 'waiting to attack', story='%s' where name = '%s'" % (rangespace,dragon)
            query2 = "update combattable set rank = 'moving' where rank='waiting to move' and combatstatus = '%s'" % (dragon)
            cursor.execute(query)
            cnx.commit()
            cursor.execute(query2)
            cnx.commit()
        elif status == 'moving' and d2status == 'waiting to attack':
            query = "update combattable set rank = 'attacking', story='%s' where name = '%s'" % (rangespace,dragon)
            query2 = "update combattable set rank = 'moving' where rank='waiting to move' and combatstatus = '%s'" % (dragon)
            cursor.execute(query)
            cnx.commit()
            cursor.execute(query2)
            cnx.commit()


        else:
            return "It's not time to move right now\nType !combat start to see the current status",dragon2,d2owner




        return('%s moved to Range %s' % (dragon.capitalize(),rangespace),dragon2,d2owner)
    else:
        dragon2 = '-123'
        d2owner = '-123'

        return('Range %s is outside your movement range.\nYou can move to %s' % (rangespace,str(davailablemoves)),dragon2,d2owner)




def movecheck(dragon1,dragon2):
    print('dragon1',dragon1)
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select owner,name,rank,story,speed from combattable where rank='moving' and (name = '%s' or  name = '%s')" % (dragon1,dragon2))
    data = []
    cursor.execute(query)
    moverange= ['A','B','C','D','E']

    for x in cursor:
        data.append(x)
    if len(data) == 0:
        return "It's not time to move right now\nType !combat start to see the current status",'-','-','-'
    #print(data[0])
    moves = 1 + int(int(data[0][4])/10)
    #moves = 2
    location = data[0][3]
    #location = 'C'
    availablemoves = []
    for x in range(0-moves,0+moves+1):
        #print('availablespace')
        #print(x)
        if moverange.index(location)+x < 0:
            pass
        else:
            #print(moverange[moverange.index(data[0][3])+x])
            availablemoves.append(moverange[moverange.index(location)+x])
    if moves == 1:
        text = '%s is located in Range %s and can move %s space' % (data[0][1],data[0][3],moves)
    else:
        text = '%s is located in Range %s and can move %s spaces' % (data[0][1],data[0][3],moves)
    #print(moverange[moverange.index(data[0][3])+moves])
    print(text)
    print(availablemoves)
    return data[0][0],data[0][1],text,availablemoves





def initative(dragon1,dragon2):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select speed from combattable where name = '%s'" % (dragon1))
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append(x[0])
    d1speed = data[0]
    query = ("select speed from combattable where name = '%s'" % (dragon2))
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append(x[0])
    d2speed = data[0]


    from random import randrange
    while True:

        roll = randrange(1,7)
        d1init = int(d1speed)+roll

        roll = randrange(1,7)
        d2init = int(d2speed)+roll
        if d1init == d2init:
            if d1speed == d2speed:
                pass
            else:
                if int(d1speed) > int(d2speed):
                    text = 'There was a tie\n%s attacks first based on speed score' % dragon1
                    text2 = '%s moves first' % dragon1
                    text = text + '\n'+ text2
                    query = "update combattable set rank = 'waiting to move' where name = '%s'" % (dragon1)
                    query2 = "update combattable set rank = 'moving' where name = '%s'" % (dragon2)
                    cursor.execute(query)
                    cursor.execute(query2)
                    cnx.commit()


                else:
                    text = 'There was a tie\n%s attacks first based on speed score' % dragon2
                    text2 = '%s moves first' % dragon1
                    text = text + '\n'+ text2
                    query = "update combattable set rank = 'waiting to move' where name = '%s'" % (dragon2)
                    query2 = "update combattable set rank = 'moving' where name = '%s'" % (dragon1)
                    cursor.execute(query)
                    cursor.execute(query2)
                    cnx.commit()

                d1 = '%s - initative is %s' % (dragon1,d1init)
                d2 = '%s - initative is %s' % (dragon2,d2init)
                return '```'+text+'\n'+d1+'\n'+d2+'```'
        else:
            break

    d1 = '%s - initative is %s' % (dragon1,d1init)
    d2 = '%s - initative is %s' % (dragon2,d2init)
    if int(d1init)>int(d2init):
        text = '%s attacks first' % dragon1
        text2 = '%s moves first' % dragon2
        text = text + '\n'+ text2
        query = "update combattable set rank = 'waiting to move' where name = '%s'" % (dragon1)
        query2 = "update combattable set rank = 'moving' where name = '%s'" % (dragon2)
        cursor.execute(query)
        cursor.execute(query2)
        cnx.commit()

    else:
        text = '%s attacks first' % dragon2
        text2 = '%s moves first' % dragon1
        text = text + '\n'+ text2
        query = "update combattable set rank = 'waiting to move' where name = '%s'" % (dragon2)
        query2 = "update combattable set rank = 'moving' where name = '%s'" % (dragon1)
        cursor.execute(query)
        cursor.execute(query2)
        cnx.commit()


    return '```'+text+'\n'+d1+'\n'+d2+'```'


def randomevents(dragonname):

    from random import randrange
    roll = randrange(1,7)
    if roll != 1:
        return '```%s rolled a %s\n\nNo random events ```' % (dragonname,str(roll))
    else:
        roll2 = randrange(1,7)
        if roll2 == 1:
            event = 'Attacked by slayers'
        if roll2 == 2:
            event = 'Wrath of Gaia'
        if roll2 == 3:
            event = 'Call of Shalkith'
        if roll2 == 4:
            event = 'Breath of Gaia'
        if roll2 == 5:
            event = 'Wisdom of the Ancients'
        if roll2 == 6:
            event = 'The Sage Towers'

        return '```%s rolled a %s\n\nRandom Event Triggered\n%s\n```' % (dragonname,str(roll),event)




def regainessence(defender,attacker):
    defender,attacker = dragonstats(defender,attacker)
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)


    if defender[2] == 'starting' and attacker[2] == 'starting':

        regen,maximumes = regenessence(defender[1],defender[6])
        defess = str(min(int(defender[27])+regen,maximumes))
        print(defender)
        print(regen,maximumes)
        print(defess)
        regen,maximumes = regenessence(attacker[1],attacker[6])
        attess = str(min(int(attacker[27])+regen,maximumes))
        print(attacker)
        print(regen,maximumes)
        print(attess)

        query = ("update combattable set essence = '%s' where name = '%s'" % (defess,defender[1]))
        cursor.execute(query)
        cnx.commit()
        query = ("update combattable set essence = '%s' where name = '%s'" % (attess,attacker[1]))
        cursor.execute(query)
        cnx.commit()
        print(attacker[1],attess,defender[1],defess)
        text = '```Regaining Essense:\n\n%s has %s essence\n%s has %s essence```' % (attacker[1],attess,defender[1],defess)

        return text

    '''
    1. regen Essence
    2. roll for random events
    3. initative
        range
        combat round begins
    4. dragon announces intent
    5. roll to see if intent is a success
    6. Damage resolve
        combat round ends
    7. repeat 4-6 for other dragons
        turn ends


    '''

    min(int(defender[27])+regen,maximumes)


def regenessence(dragonname,age):
    import math
    regennum = math.ceil(int(age)/2)
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select essence from dragons where name = '%s'" % (dragonname))
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append(x[0])

    return regennum,int(data[0]) # regen max


def dragonstats(defender,attacker):

    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select * from combattable where name = '%s'" % (attacker))
    attackerdata = []
    cursor.execute(query)
    for x in cursor:
        attackerdata.append([x])

    query = ("select * from combattable where name = '%s'" % (defender))
    defenderdata = []
    cursor.execute(query)
    for x in cursor:
        defenderdata.append([x])

    return attackerdata[0][0],defenderdata[0][0]

def combatcommand(message):
    owner = message.author.id
    import mysql.connector
    import creds

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)


    query = ("select * from combattable where owner = '%s'" % (owner))
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append([x])
    text = message.content.lower().split('!combat ')[1]
    print(message.content)
    if len(data) == 0:
        return 'Somthing went wrong. you dont have an open challenge and shouldnt be able to type here\n<@272169658440744960> please fix'

    if 'start' in text.lower():
        print('attempting to start')
        defender = data[0][0][3]
        attacker = data[0][0][1]

        query = ("select * from combattable where name = '%s' and combatstatus = '%s'" % (defender,attacker))
        data = []
        cursor.execute(query)
        for x in cursor:
            data.append([x])

        if len(data) > 0:
            continuefight = True
        else:
            return defender+' has not accepted the challenge yet','-','-','-','-'

        query = ("select * from combattable where name = '%s' or name = '%s'" % (defender,attacker))
        ddata = []
        cursor.execute(query)
        for x in cursor:
            ddata.append(x)



        try:
            int(data[0][0][2])
            inprogress = False
        except:
            print()
            print(ddata[1][3])
            #print(combatstatus(defender,attacker))
            if ddata[1][2] == 'starting' and ddata[0][2] == 'starting':
                return 'Combat starting test now\n %s %s' % (ddata[0][1]+' '+ddata[0][2],ddata[1][1]+' '+ddata[1][2]),ddata[0][2],ddata[0][1],ddata[1][2],ddata[1][1]
            else:
                text = '%s\nLife: %s\nEssence: %s\nStatus: %s\nRange: %s' % (ddata[0][1].capitalize(),ddata[0][17],ddata[0][27],ddata[0][2],ddata[0][25])
                text2 =  '%s\nLife: %s\nEssence: %s\nStatus: %s\nRange: %s' % (ddata[1][1].capitalize(),ddata[1][17],ddata[1][27],ddata[1][2],ddata[1][25]) + '\n\n' + text
                return "```"+'Combat already started\nCurrent Status:\n\n'+text2+"```",'-','-','-','-'


        #if data[0][0][2] == 'starting' or data[0][0][2] == 'complete':
        #    return 'Combat already in progress'


        query = ("update combattable set rank = 'starting' where name = '%s' or name = '%s'" % (defender,attacker))

        cursor.execute(query)
        cnx.commit()

        #print(combatstatus(defender,attacker))

        #return combatstatus(defender,attacker)
        text = '%s\nLife: %s\nEssence: %s' % (ddata[0][1].capitalize(),ddata[0][17],ddata[0][27])
        text2 =  '%s\nLife: %s\nEssence: %s' % (ddata[1][1].capitalize(),ddata[1][17],ddata[1][27]) + '\n\n' + text
        return "```"+'Starting Combat \nCombat progress:\n\n'+text2+"```",'starting',ddata[0][1],'starting',ddata[1][1]

    return 'test','-','-','-','-'



def battleroom(type,dragonname):
    from lookups import battlefield
    import discord
    from discord.utils import get
    battlefields = battlefield()
    #print(battlefields)
    taglist = []
    openfields = []
    for x in battlefields:
        taglist.append(x[0])
        if x[3] == 'open':
            openfields.append([x[0],x[1]])
    changeneeded = True

    bf = openfields[0][0]
    bfname = openfields[0][1]


    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("update battlefields set status ='%s' where tag = '%s'" % ('in use',bf))
    cursor.execute(query)
    cnx.commit()

    return bf,bfname

def newchallange(challanger,defender):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    try:
        challanger+0
        npc = False
    except:
        #print('NPC IS TRUE')
        npc = True

    if npc == False:


        query = ("select * from dragons where retired ='0' and owner='%s'" % (challanger))

        data = []
        cursor.execute(query)
        for x in cursor:
            data.append([x])

        if len(data) <1:
            return '<@%s> you must hatch a dragon before you can make a challenge' % challanger,'-','-','-','-','-'
        for x in data:
            #print(x)
            challanger = x[0][1]
        #print('dragon name ',challanger)

        query = ("select * from combattable where name ='%s' or combatstatus ='%s' or  name ='%s' or combatstatus ='%s'" % (challanger,challanger,defender,defender))
        print(query)
        data = []
        cursor.execute(query)
        defending = ''
        attacking = ''
        for x in cursor:
            data.append([x])
        for x in data:
            defending = x[0][3]
            attacking = x[0][1]

        if defending.capitalize() == defender.capitalize() and attacking.capitalize() == challanger.capitalize():
            print('keep moving')
            message = challanger.capitalize()+' is already in combat with '+defending.capitalize()
            return message,'-','-','-','-','-'
        elif defending.capitalize() == challanger.capitalize() and attacking.capitalize() != defender.capitalize():
            print('keep moving')
            message = challanger.capitalize()+' is already in combat with '+defending.capitalize()
            return message,'-','-','-','-','-'

        print('data!!!!!',data)
        if len(data) > 0:
            if attacking.capitalize() == challanger.capitalize():
                message = challanger.capitalize()+', you are already in combat with '+defending.capitalize()
                return message,'-','-','-','-','-'
            elif attacking.capitalize() != challanger.capitalize() and defending.capitalize() != challanger.capitalize():
                #return and announce already has active challenge
                message = defending.capitalize()+' is already being challenged by '+attacking.capitalize()
                return message,'-','-','-','-','-'



        query = ("select * from dragons where name ='%s' or name ='%s'" % (challanger,defender))
        print(query)

        rdata = []
        cursor.execute(query)
        for x in cursor:
            #print(x)
            rdata.append(int(x[2]))

        rdata.sort()
        if rdata[1]-rdata[0]>5:
            message = 'You can not challenge %s, that Dragon is outside your 5 rank challenge limit' % defender.capitalize()
            return message,'-','-','-','-','-'

        else:
            #continue
            message = challanger,'not in combat'
    else:
        pass

    query = ("select * from combattable where combatstatus ='%s'" % (challanger))
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append([x])


    if len(data) > 0:
        #print(data[0][0])
        attacker = data[0][0][1]
        #print(defender)
        #print(data[0][0][1].lower(),defender.lower())
        #input(data[0][0][1].lower() == defender.lower())
        if data[0][0][1].lower() == defender.lower():

            message = challanger.capitalize()+' has accepted a challenge from '+attacker.capitalize()+'! <@%s>' % data[0][0][0]
            query = ("insert into combattable select * from dragons where retired = '0' and name = '%s'" % (challanger.capitalize()))
            #print(query)
            cursor.execute(query)
            cnx.commit()

            query = "update combattable set story='A' where name = '%s'" % (challanger.capitalize())
            query2 = "update combattable set story='A' where name = '%s'" % (attacker.capitalize())
            cursor.execute(query)
            cnx.commit()



            bf = data[0][0][26]
            query = ("update combattable set battlecry = '%s', combatstatus = '%s' where name = '%s'" % (data[0][0][26],attacker,challanger))
            #print(query)
            cursor.execute(query)
            cnx.commit()

            query = ("select owner from dragons where retired = '0' and name = '%s'" % (attacker))
            data = []
            adata = []

            cursor.execute(query)
            for x in cursor:
                data.append([x])
                adata.append([x[0]])


#            aquery = ("select owner from dragons where retired = '0' and name = '%s'" % (attacker))
#            adata = []
#            cursor.execute(aquery)
#            for x in cursor:
#                adata.append([x[0]])

            dquery = ("select owner from dragons where retired = '0' and name = '%s'" % (challanger))
            ddata = []
            cursor.execute(dquery)
            for x in cursor:
                ddata.append([x[0]])










            #message = challanger.capitalize()+' has challanged '+defender.capitalize()+'!\n<@%s> must accept this before combat can begin.' % data[0][0][0]
            return message,'assign',adata[0],ddata[0],bf,'-'

        else:
            message = challanger.capitalize()+', you are already in combat with '+attacker.capitalize()+' '
            return message,'-','-','-','-','-'
        #return and announce already has active challenge
        message = challanger+', you are already in combat with '+attacker+' '
    else:
        #continue
        message = challanger.capitalize()+' has challanged '+defender.capitalize()+' '
        #print(message)


    query = ("insert into combattable select * from dragons where retired = '0' and name = '%s'" % (challanger))
    #print(query)
    cursor.execute(query)
    cnx.commit()

    bf,bfname = battleroom('challenge',challanger)
    #print('battlefield! ',bf)
    query = ("update combattable set battlecry ='%s', combatstatus = '%s' where name = '%s'" % (bf,defender,challanger))
    #print(query)
    cursor.execute(query)
    cnx.commit()

    query = ("select owner from dragons where retired = '0' and name = '%s'" % (defender))
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append([x])
    if data[0][0][0] == 'npc':
        message = challanger.capitalize()+' has entered '+ bfname +' and challenged '+defender.capitalize()+'!'
    else:
        message = challanger.capitalize()+' has entered '+ bfname +' and challenged '+defender.capitalize()+'!\n<@%s> must accept this before combat can begin.' % data[0][0][0]
    return message,data[0][0][0],challanger,defender,bf,bfname
