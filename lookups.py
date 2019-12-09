def lifeesscheck(dragon):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select life,essence from combattable where name ='%s';" % dragon)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    return data[0][0],data[0][1]


def attackstatus(dragon):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select rank from combattable where name ='%s';" % dragon)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    return data[0][0]



def enemylookup(dragon1):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select combatstatus from combattable where name ='%s';" % dragon1)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)

    query = ("select owner from combattable where name ='%s';" % data[0][0])
    ddata = []
    cursor.execute(query)

    for x in cursor:
            ddata.append(x)
    return ddata[0][0],data[0][0]


def dragonlookup(owner):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select name,owner from dragons where owner ='%s' and retired = '0';" % owner)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    return data[0][1],data[0][0]



def mydragon(owner):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)

    query = ("select * from dragons where owner ='%s' and retired = '0';" % owner)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)


    query = 'select * from breeds where breed = "%s"' % data[0][5]
    breeddata = []
    cursor.execute(query)
    for x in cursor:
            breeddata.append(x)

    return '''Dragon: '''+'''
Name: %s ''' % (data[0][1]) +'''
Breed: %s ''' % (data[0][5]) +'''
Rank: %s ''' % (data[0][2]) +'''

Age Cost: %s ''' % (data[0][24]) +'''
Age: %s ''' % (data[0][6]) +'''

Development Cost: %s ''' % (data[0][23]) +'''
Development Points: %s ''' % (data[0][21]) +'''
Favor: %s ''' % (data[0][22]) +'''

Wins: %s ''' % (data[0][7]) +'''
Loss: %s ''' % (data[0][8]) +'''

Attributes
Attack: %s - max %s
Defense: %s - max %s
Body: %s - max %s
Intellect: %s - max %s
Will: %s - max %s''' %  (data[0][9],breeddata[0][4],data[0][10],breeddata[0][5],data[0][11],breeddata[0][6],data[0][12],breeddata[0][9],data[0][13],breeddata[0][10])+'''
Resist: %s - max %s
Speed:%s - max %s
Discipline: %s - max %s
Essence: %s - max %s
Life: %s - max %s
\nSkills: '''% (data[0][14],breeddata[0][11],data[0][15],breeddata[0][7],data[0][16],breeddata[0][12],data[0][27],breeddata[0][13],data[0][17],breeddata[0][8])+'''
Claw Attack: %s - costs 1 essence
Tail Bash: %s - costs %s essence''' %(data[0][18].split('claw attack:')[1].split(',')[0],data[0][11],data[0][11])













def roller(dice):

    from random import randrange
    rolls = []
    for x in range(0,dice):
        roll = randrange(1,7)
        rolls.append(roll)
        while roll == 6:
            roll = randrange(1,7)
            rolls.append(roll)
    return rolls


def fixrank(dragonname):
    #select rank,name,breed,win,loss from dragons order by convert(substring(rank,1), integer) asc;
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select rank,name from dragons where retired = '0' order by convert(substring(rank,1), integer) asc;")
    data = []
    cursor.execute(query)
    for x in cursor:
        data.append([x[0],x[1]])


    rank = data
    if dragonname == True:
        for x in rank:
            if str(rank.index(x)+1) != x[0]:
                if x[1] == dragonname:
                    dragonrank = str(rank.index(x)+1)

                    query = 'update dragons set rank = "%s" where name = "%s"' % (str(rank.index(x)+1),x[1])
                    cursor.execute(query)
                    cnx.commit()

                else:
                    dragonrank = str(rank.index(x)+1)
                    query = 'update dragons set rank = "%s" where name = "%s"' % (str(rank.index(x)+1),x[1])
                    cursor.execute(query)
                    cnx.commit()

        return rank
    else:
        pass

    for x in rank:
        if str(rank.index(x)+1) != x[0]:
            if x[1] == dragonname:
                dragonrank = str(rank.index(x)+1)

                query = 'update dragons set rank = "%s" where name = "%s"' % (str(rank.index(x)+1),x[1])
                cursor.execute(query)
                cnx.commit()

    return dragonrank




def dlist():
    #select rank,name,breed,win,loss from dragons order by convert(substring(rank,1), integer) asc;
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select name from dragons order by convert(substring(rank,1), integer) asc;")
    data = []
    cursor.execute(query)
    for x in cursor:
        try:
            data.append(x[0].lower())
        except:
            data.append(x[0])
    query = ("select name from dragonhatching order by convert(substring(rank,1), integer) asc;")

    cursor.execute(query)
    for x in cursor:
        try:
            data.append(x[0].lower())
        except:
            data.append(x[0])


    return data



def dragonlatter():
    #select rank,name,breed,win,loss from dragons order by convert(substring(rank,1), integer) asc;
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select rank,name,breed,win,loss from dragons order by convert(substring(rank,1), integer) asc;")
    data = []
    cursor.execute(query)
    data.append(['#','Name','Breed','W','L'])
    data.append(['-','-','-','-','-'])

    for x in cursor:
            data.append([x[0],x[1],x[2],x[3],x[4]])


    return data


def battlefield():
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from battlefields")
    data = []
    cursor.execute(query)

    for x in cursor:
            data.append([x[0],x[1],x[2],x[3]])


    return data


def challange(challanger,defender):
    import creds
    import mysql.connector

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from dragons where retired = '0'")
    data = []
    cursor.execute(query)
    challangerdragon = []
    defenderdragon = []
    print('challange')
    print(challanger)
    print(defender)

    for x in cursor:
        if str(challanger) in x:
            challangerdragon = x
        if str(defender) in x:
            defenderdragon = x

    return challangerdragon,defenderdragon



def joinbattle(message):
    from discord.utils import get
    battlefields = battlefield()
    print(battlefields)
    taglist = []
    openfields = []
    for x in battlefields:
        taglist.append(x[0])
        if x[3] == 'open':
            openfields.append([x[0],x[1]])
    changeneeded = True
    for x in message.author.roles:
        print(x)
        if str(x) in taglist:
            print(x)
            changeneeded = False
        bf = openfields[0][0]
        bfname = openfields[0][1]
        from discord.utils import get
        role = get(message.guild.roles, name=bf)
    if changeneeded == True:
        return changeneeded,bfname,role,bf
    else:
        return changeneeded,bfname,'',''

def leavebattle(message):
    from discord.utils import get
    battlefields = battlefield()
    print(battlefields)
    taglist = []
    for x in battlefields:
        taglist.append([x[0],x[1]])
    changeneeded = True
    for x in message.author.roles:
        for y in taglist:
            if str(x) in y:
                changeneeded = False
                bf = y[0]
                bfname = y[1]
                role = get(message.guild.roles, name=bf)

    if changeneeded == False:
        return changeneeded,role,bf,bfname
        #await discord.Member.remove_roles(message.author, role)
        #await message.channel.send('removed '+bf+' role from '+str(usernick)+' removed from '+bfname)
    else:
        return changeneeded,'','',''
        #await message.channel.send(str(usernick)+", you're not in a battlefield")
