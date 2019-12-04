
def starthatch(message):



    def skillcheck(owner,comments):
        import creds
        import mysql.connector

        u = creds.mysqlun # MySQL username
        p = creds.mysqlpw # MySQL password
        h = creds.mysqlhost # MySQL server
        db = 'shalkith' # MySQL datanase name
        cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
        cursor = cnx.cursor(buffered=True)

        attribs = [
        ['attack','attack'],
        ['defense','defense'],
        ['body','body'],
        ['intellect','inti'],
        ['will','will'],
        ['resist','resist'],
        ['speed','speed'],
        ['discipline','disc'],
        ['life','life'],
        ['essence','essence'],
        ]
        for x in attribs:
            if x[0] == comments.lower():
                print('x data matched!!',x)
                attrib = x[1]

        query = 'select breed,%s from dragonhatching where owner = "%s"' % (attrib,owner)
        attribdata = []
        cursor.execute(query)
        for x in cursor:
                attribdata.append(x)

        currentskillevel = attribdata[0][1]
        breed = attribdata[0][0]

        query = 'select %smax from breeds where breed = "%s"' % (comments.lower(),breed)
        attribdata = []
        cursor.execute(query)
        for x in cursor:
                attribdata.append(x)

        maxskilllevel = attribdata[0][0]
        newskilllevel = int(currentskillevel) + 1
        if newskilllevel > int(maxskilllevel):
            return False,'0',attrib
        else:
            return True,str(newskilllevel),attrib




    def nextstep(step):
        query = ("select * from dragonhatching where owner ='%s' and retired = '0';" % owner)
        data = []
        cursor.execute(query)
        for x in cursor:
                data.append(x)


        query = 'select * from breeds where breed = "%s"' % data[0][5]
        breeddata = []
        cursor.execute(query)
        for x in cursor:
                breeddata.append(x)


        if step == 'name':
            return 'Type !hatch name to name your dragon \n Example: !hatch Yanthas '
        elif step == 'complete':
            return 'Type !hatch complete to join the battle'
        elif step == 'breed':
            return 'Type !hatch breedtype to select your breed \n Example: \n!hatch Blue\n!hatch Red\n!hatch Brown\n!hatch Silver'
        elif step == 'advancement':
            return '''Next step
Type !hatch stat to advance your Attributes, Skills or Spells\n
Example: \n!hatch attack\n!hatch claw attack\n\n
Attributes
Attack (current %s, max %s)
Defense (current %s, max %s)
Body (current %s, max %s)
Intellect (current %s, max %s)
Will (current %s, max %s)''' %  (data[0][9],breeddata[0][4],data[0][10],breeddata[0][5],data[0][11],breeddata[0][6],data[0][12],breeddata[0][9],data[0][13],breeddata[0][10])+'''
Resist (current %s, max %s)
Speed (current %s, max %s)
Discipline (current %s, max %s)
Essence (current %s, max %s)
Life (current %s, max %s)
\nSkills (can't be improved beyond your discipline rating)'''% (data[0][14],breeddata[0][11],data[0][15],breeddata[0][7],data[0][16],breeddata[0][12],data[0][27],breeddata[0][13],data[0][17],breeddata[0][8])+'''
Claw Attack (current %s, costs 1 essense)
Tail Bash (Increases with Body, costs 'body score' essense)
\nYou have %s advancement points to use''' %(data[0][18].split('claw attack:')[1].split(',')[0],data[0][21])


    pass


    import creds
    import mysql.connector

    if message.author.nick == None:
        username = message.author.name
    else:
        username = message.author.nick

    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'shalkith' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    owner = str(message.author.id)
    query = ("select name from dragons where owner ='%s' and retired = '0';" % owner)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    if len(data)>0:
        dragonname = data[0][0]
        return '%s, you already have a dragon named "%s". This dragon must be retired before you can hatch a new one.' % (username,dragonname)

    query = ("select * from dragonhatching where owner ='%s' and retired = '0';" % owner)
    data = []
    cursor.execute(query)
    for x in cursor:
            data.append(x)
    if len(data)>0:
        if 'nextstep' in message.content:
            return nextstep(data[0][3])
        else:
            try:
                comments = message.content.split('!hatch ')[1]
            except:
                return nextstep(data[0][3])

            if data[0][3] == 'complete' or data[0][3] == 'available':
                if comments.lower() == 'complete':
                    print('getting dragton ready to move')
                    query = 'update dragonhatching set DP = "0", combatstatus = "available" where owner = "%s"' % (owner)
                    cursor.execute(query)
                    cnx.commit()
                    print('moving dragon')
                    query = 'insert into dragons select * from dragonhatching where owner = "%s"' % (owner)
                    cursor.execute(query)
                    cnx.commit()
                    print('deleting from hatching table')
                    query = 'delete from dragonhatching where owner = "%s"' % (owner)
                    cursor.execute(query)
                    cnx.commit()

                    from lookups import fixrank
                    rank = fixrank(data[0][1])
                    return "A new Dragon has entered the world to compete for the title of Shalkith\nName: "+data[0][1]+"\nBreed: "+data[0][5]+"\nRank: "+rank


                else:
                    return nextstep(data[0][3])

            if data[0][3] == 'name':
                validname = True
                charlist = ['-',"'",]
                from lookups import dlist
                dragons = dlist()
                for a in comments:
                    if a.isalpha() or a in charlist:
                        pass
                    else:
                        validname = False

                if comments.lower() in dragons:
                    return 'Dragon name ('+comments+') is already taken. '

                if validname == False:
                    return "Valid names must contain only Alphabetical characters or: - and '"

                query = 'update dragonhatching set name = "%s", combatstatus = "breed" where owner = "%s"' % (comments.capitalize(),owner)
                cursor.execute(query)
                cnx.commit()
                return "Dragon name set to %s \n Next step: \nType !hatch breedtype to select your breed \n Example: \n!hatch Blue\n!hatch Red\n!hatch Brown\n!hatch Silver" % comments
            if data[0][3] == 'breed':
                print('comments'+comments)
                if comments.lower() not in ['red','blue','silver','brown']:
                    return nextstep(data[0][3])
                query = 'select * from breeds where breed = "%s"' % comments.lower().capitalize()
                breeddata = []
                cursor.execute(query)
                for x in cursor:
                        breeddata.append(x)
                query = 'update dragonhatching set skills="tail bash,claw attack:1,",breed="%s",attack="%s",defense="%s",body="%s",inti="%s",will="%s",resist="%s",speed="%s",disc="%s",improvement_cost="%s",age_cost="%s",DP="%s",combatstatus = "advancement" where owner = "%s"' % (comments.lower().capitalize(),'0','0','0','0','0','0','0','0',breeddata[0][2],breeddata[0][1],breeddata[0][3],owner)
                cursor.execute(query)
                cnx.commit()
                nxt = nextstep('advancement')
                print(nxt)
                return "Dragon breed set to "+comments.lower().capitalize()+" \n\n" +nxt
                #return "Dragon breed set to %s \n\n Next step: \nType !hatch skilltoadvance to advance your skills \n Example: \n!hatch attack\n!hatch defense\n!hatch body\n!hatch speed\n!hatch intellect\n!hatch will\n!hatch resist\n!hatch essense\n" % comments

            if data[0][3] == 'advancement':
                print('advancements')
                print('comments'+comments)
                improvetype = 'none'
                attributes = ['attack','defense','body','intellect','will','resist','discipline','speed','essence','life']
                skills = ['claw attack','tail bash']
                spells = []
                if comments.lower() in attributes:
                    improvementcheck,newskill,attrib = skillcheck(data[0][0],comments)
                    if improvementcheck == False:
                        return comments.lower().capitalize()+' is already at its max'
                    else:

                        query = 'update dragonhatching set %s = "%s" where owner = "%s"' % (attrib,newskill,data[0][0])
                        cursor.execute(query)
                        cnx.commit()
                        advpoints = str(int(data[0][21]) - 1)
                        query = 'update dragonhatching set DP = "%s" where owner = "%s"' % (advpoints,data[0][0])
                        cursor.execute(query)
                        cnx.commit()

                        if advpoints == '0':
                            query = 'update dragonhatching set combatstatus = "complete" where owner = "%s"' % (owner)
                            cursor.execute(query)
                            cnx.commit()
                            return comments.lower().capitalize()+' increased.\n\n'+nextstep('complete')



                        return comments.lower().capitalize()+' increased.\n\n'+nextstep(data[0][3])




                        return comments.lower().capitalize()+' would be improved to ' + newskill
                    improvetype = 'attribute'
                elif comments.lower() in skills:
                    if comments.lower() == 'tail bash':
                        return 'Tail Bash is improved by improving your body'
                    else:
                        oldlevel = int(data[0][18].split(comments.lower()+':')[1].split(',')[0])
                        newlevel = oldlevel +1
                        print('newlevel'+str(newlevel),data[0][16])
                        print(newlevel > int(data[0][16]))
                        if newlevel > int(data[0][16]):
                            return 'You must improve your discipline before you can raise '+comments.lower().capitalize()+' any higher'
                        else:
                            newskills = data[0][18].split(comments.lower()+':')[0]+comments.lower()+':'+str(newlevel)+','+data[0][18].split(comments.lower()+':')[1].split(',')[1]
                            query = 'update dragonhatching set skills = "%s" where owner = "%s"' % (newskills,data[0][0])
                            cursor.execute(query)
                            cnx.commit()
                            advpoints = str(int(data[0][21]) - 1)
                            query = 'update dragonhatching set DP = "%s" where owner = "%s"' % (advpoints,data[0][0])
                            cursor.execute(query)
                            cnx.commit()

                            if advpoints == '0':
                                query = 'update dragonhatching set combatstatus = "complete" where owner = "%s"' % (owner)
                                cursor.execute(query)
                                cnx.commit()
                                return comments.lower().capitalize()+' increased to '+str(newlevel)+'.\n\n'+nextstep('complete')


                            return comments.lower().capitalize()+' increased to '+str(newlevel)+'.\n\n'+nextstep(data[0][3])

                        print('skill',str(int(data[0][21])))
                        print('skill',str(int(data[0][21]) - 1))
                        improvetype = 'skill'
                elif comments.lower() in spells:
                    improvetype = 'spell'

                if improvetype == 'none':
                    return 'I didnt understand your command. Please try again.\n\n'+nextstep(data[0][3])
                else:
                    return 'This will improve a '+improvetype


    else:
        query = 'insert into dragonhatching (owner,rank,combatstatus,retired,age,win,loss,life,essence) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (owner,'999','name','0','1','0','0','5','1')
        cursor.execute(query)
        cnx.commit()
        return 'Dragon creation started.\n Next step: \nType !hatch name to name your dragon \n Example: !hatch Yanthas \n type !hatch nextstep if you need to be reminded what to do next'





    #return 'test reply'
