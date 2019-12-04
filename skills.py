#attack('npc','Trillye','npc','Yanthas',tailbash('npc','Trillye')[1])
# combatai(2,3,'npc','jerk','npc','trogdor')

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
        if healchance < 20 and healcost <= essense:
            print('dragon is healing')
            heal(attackid,attackname,currentlife,healcost)
        elif essense >= body and attackchoice > 20 and body > 0:
            print('tailbash')
            attack(attackid,attackname,defendid,defendname,tailbash(attackid,attackname)[1])
        else:
            print('clawattack')
            attack(attackid,attackname,defendid,defendname,clawattack(attackid,attackname)[1])

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

    print(name+' healed for ' + str(healing) + ' life went from '+str(currentlife)+' to '+str(newcurrentlife)+'. max life is '+life)

def attack(attuserid,attacker,defuserid,defender,damage):
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
        query = ("select speed from,attack dragons where owner ='%s' and retired = '0';" % attuserid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)

    adata = data[0][0]

    acombatdice =  math.floor(int(adata)/10) +1
    acombatdice = sum(roller(acombatdice))
    attackvalue = int(data[0][1])
    attackvalue = acombatdice + attackvalue
    print('attack',attackvalue)

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
    dcombatdice = sum(roller(dcombatdice))
    defensevalue = int(data[0][1])
    body = int(data[0][2])
    defensevalue = dcombatdice + defensevalue
    print('defense',defensevalue)

    if attackvalue > defensevalue:
        print('attacker wins')
        damage=max(1,damage-int(body))
        print(damage,'damage delt')
    else:
        print('defender wins')




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
    return str(result)+' + '+bonus,sum(result)+int(bonus)

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
    if userid == 'npc':
        query = ("select body from dragons where name ='%s' and retired = '0';" % name)
    else:
        query = ("select body from dragons where owner ='%s' and retired = '0';" % userid)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    data = data[0][0]
    skilllevel = data
    dice = damagechart(skilllevel,damagecode)
    bonus = '0'
    if '+' in dice:
        dice,bonus = dice.split('+')
    result = roller(int(dice))
    print(str(result)+' + bonus: '+bonus,sum(result)+int(bonus))
    return str(result)+' + '+bonus,sum(result)+int(bonus)
