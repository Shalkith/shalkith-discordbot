#attack('npc','Trillye','npc','Yanthas',tailbash('npc','Trillye')[1])
# combatai(2,3,'npc','jerk','npc','trogdor')

availableskills = ['pass','claw attack','tail bash','heal']

def combatai(essense,currentlife,attackid,attackname,defendid,defendname):
    import creds
    from random import randrange
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    if attackid == 'npc':
        query = ("select body,life from dragons where name ='%s' and retired = '0';" % attackname)
    else:
        query = ("select body,life from dragons where owner ='%s' and retired = '0';" % attackid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    life = int(data[0][1])
    body = int(data[0][0])

    lp = currentlife/life
    healchance = randrange(0,(100*lp)+1)
    healcost = (life-currentlife)*2
    attackchoice = randrange(0,101)

    while healcost > essense:
        healcost = healcost - 2


    if essense > 0:
        if healchance < 20 and healcost <= essense and currentlife != life and essence > 1:
            print('dragon is healing')
            text1 = '%s uses heal!\n' % attackname
            text = heal(attackid,attackname,currentlife,healcost)
        elif essense >= body and attackchoice > 20 and body > 0:
            print('tailbash')
            skill = tailbash(attackid,attackname)
            text1 = '%s uses Tailbash!\n' % attackname
            text = attack(attackid,attackname,defendid,defendname,skill[1],skill[2])
        else:
            print('clawattack')
            skill = clawattack(attackid,attackname)
            text1 = '%s uses Claw Attack!\n' % attackname
            text = attack(attackid,attackname,defendid,defendname,skill[1],skill[2])
        return text1+text
    else:
        text = '%s must pass no essense' % attackname
        return text

        #clawattack 2 essense
        #tailbash body essense
        #heal 1hp per 2 essense


def heal(userid,name,currentlife,essense):
    import creds
    import math
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    if userid == 'npc':
        query = ("select life from dragons where name ='%s' and retired = '0';" % name)
    else:
        query = ("select life from dragons where owner ='%s' and retired = '0';" % userid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    life = data[0][0]
    healing = math.floor(essense/2)

    newcurrentlife = min(healing + currentlife,int(life))

    query = 'update combattable set rank="starting", life = "%s", essence="%s" where name = "%s"' % (str(newcurrentlife),essense,name)
    cursor.execute(query)
    cnx.commit()



    query = ("select combatstatus from combattable where name ='%s'" % name)
    cursor.execute(query)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    defender = data[0][0]



    query = ("select rank from combattable where name ='%s'" % defender)

    cursor.execute(query)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    defstatus = data[0][0]
    if defstatus == 'waiting to attack':
        query = 'update combattable set rank="attacking" where name = "%s"' % (defender)
        nextstep = ''
    else:
        query = 'update combattable set rank="starting" where name = "%s"' % (defender)
        nextstep = '\n\ntype !combat start to start the next round'
    cursor.execute(query)
    cnx.commit()




    #return = name+' healed for ' + str(healing) + ' life went from '+str(currentlife)+' to '+str(newcurrentlife)+'. max life is '+life
    return '%s healed for %s. Life went from %s to %s. max life is %s' % (name,healing,currentlife,newcurrentlife,life) + nextstep


def attack(attuserid,attacker,defuserid,defender,damage,esscost):
    from lookups import roller
    # combat dice =  (dragonspeed /10) +1
    import math
    #math.floor(0.6)
    import creds
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    if attuserid == 'npc':
        query = ("select speed,attack from dragons where name ='%s' and retired = '0';" % attacker)
    else:
        query = ("select speed,attack from dragons where owner ='%s' and retired = '0';" % attuserid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)

    adata = data[0][0]

    acombatdice =  math.floor(int(adata)/10) +1
    totalcombatdice = acombatdice
    rolls = roller(acombatdice)
    acombatdice = sum(rolls)
    attackvalue = int(data[0][1])
    attackscore = attackvalue
    attackvalue = acombatdice + attackvalue
    print('attack',attackvalue)

    atext = '%s has %s combat dice\nRolled: %s +(Attack skill of %s)\nTotal: %s' % (attacker,totalcombatdice,str(rolls),attackscore,attackvalue)

    if defuserid == 'npc':
        query = ("select speed,defense,body from dragons where name ='%s' and retired = '0';" % defender)
    else:
        query = ("select speed,defense,body from dragons where owner ='%s' and retired = '0';" % defuserid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    ddata = data[0][0]
    dcombatdice =  math.floor(int(ddata)/10) +1
    dtotalcombatdice = dcombatdice
    rolls = roller(dcombatdice)
    dcombatdice = sum(rolls)
    defensevaluelist = int(data[0][1])
    defensescore = defensevaluelist
    body = int(data[0][2])
    defensevalue = dcombatdice + defensevaluelist

    dtext = '%s has %s combat dice\nRolled: %s +(Defense skill of %s)\nTotal: %s' % (defender,dtotalcombatdice,str(rolls),defensevaluelist,defensevalue)


    alltext = atext+'\n\n'+dtext+'\n\n'

    if attackvalue > defensevalue:
        maxdamage = damage
        damage=max(1,damage-int(body))

        query = ("select essence from combattable where name='%s';" % attacker)
        data = []
        cursor.execute(query)
        for x in cursor:
                data.append(x)

        ess = data[0][0]
        if int(esscost) > int(ess):
            text = '%s doesnt have enough available Essence to use this skill\nSkill cost:%s\nCurrent Essence:%s' % (attacker,esscost,ess)
            nextstep = ''
        else:
            newess = str(int(ess) - int(esscost))
            attackerquery = 'update combattable set rank="starting", essence="%s" where name = "%s"' % (newess,attacker)

            cursor.execute(attackerquery)
            cnx.commit()

            query = ("select life,rank from combattable where name='%s';" % defender)
            data = []
            cursor.execute(query)
            for x in cursor:
                    data.append(x)
            deflife = data[0][0]
            defstatus = data[0][1]

            newlife = int(deflife) - int(damage)
            if defstatus == 'waiting to attack':
                query = 'update combattable set rank="attacking", life="%s" where name = "%s"' % (str(newlife),defender)
                nextstep = ''
            else:
                query = 'update combattable set rank="starting", life="%s" where name = "%s"' % (str(newlife),defender)
                nextstep = '\n\ntype !combat start to start the next round'
            cursor.execute(query)
            cnx.commit()


            text = '%s has done %s (%s Max damage and %s soak from defenders body skill) damage to %s with its attack!' % (attacker,damage,maxdamage,body,defender)
            text = text + '\n%s has %s life remaining' % (defender,str(newlife))

            text = alltext + text

            if newlife < 1:
                text = text + '\n%s has defeated %s!' % (attacker,defender)
                query = 'update combattable set rank="winner" where name = "%s"' % (attacker)
                query2 = 'update combattable set rank="loser" where name = "%s"' % (defender)
                nextstep = '\n\nType !combat end to end combat'

                cursor.execute(query)
                cursor.execute(query2)
                cnx.commit()

    else:
        print('defender wins')
        text = '%s misses %s with its attack!' % (attacker,defender)
        text = alltext + text
        newesscost = int(esscost/2)
        query = 'update combattable set rank="starting",essence ="%s" where name = "%s"' % (str(newesscost),attacker)
        cursor.execute(query)
        cnx.commit()


        query = ("select life,rank from combattable where name='%s';" % defender)
        data = []
        cursor.execute(query)
        for x in cursor:
                data.append(x)
        deflife = data[0][0]
        defstatus = data[0][1]

        if defstatus == 'waiting to attack':
            query = 'update combattable set rank="attacking" where name = "%s"' % (defender)
            nextstep = ''
        else:
            query = 'update combattable set rank="starting" where name = "%s"' % (defender)
            nextstep = '\n\ntype !combat start to start the next round'
        cursor.execute(query)
        cnx.commit()


    return text+nextstep



def damagechart(skilllevel,damagecode):
    import creds
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select dice from damagechart where level ='%s' and damagecode = '%s';" % (skilllevel,damagecode))
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    data = data[0][0]
    return data

def clawattack(userid,name):
    from lookups import roller
    damagecode = 'e'
    import creds
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    if userid == 'npc':
        query = ("select skills from dragons where name ='%s' and retired = '0';" % name)
    else:
        query = ("select skills from dragons where owner ='%s' and retired = '0';" % userid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    data = data[0][0]
    skilllevel = data.split('claw attack:')[1].split(',')[0]
    dice = damagechart(skilllevel,damagecode)
    bonus = '0'
    if '+' in dice:
        dice,bonus = dice.split('+')
    result = roller(int(dice))
    print(str(result)+' + bonus: '+bonus,sum(result)+int(bonus))
    return str(result)+' + '+bonus,sum(result)+int(bonus),int(skilllevel)

def tailbash(userid,name):
    from lookups import roller
    damagecode = 'b'
    import creds
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    print(userid)
    print(name)
    if userid == 'npc':
        query = ("select body from dragons where name ='%s' and retired = '0';" % name)
    else:
        query = ("select body from dragons where owner ='%s' and retired = '0';" % userid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    print(data)
    data = data[0][0]
    skilllevel = data
    dice = damagechart(skilllevel,damagecode)
    bonus = '0'
    if '+' in dice:
        dice,bonus = dice.split('+')
    result = roller(int(dice))
    print(str(result)+' + bonus: '+bonus,sum(result)+int(bonus))
    return str(result)+' + '+bonus,sum(result)+int(bonus),int(skilllevel)
