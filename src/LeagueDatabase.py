'''
Created on Mar 19, 2014

@author: Brendan
'''

import pyodbc
import requests
import time
import tblExport


def addSummonerName(summonerName):
    summonerName = summonerName.lower()
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor()
    row = cursor.execute('SELECT summonerName from tblSummoners WHERE summonerName=?', summonerName).fetchone()
    if(row == None):
        url='https://prod.api.pvp.net/api/lol/na/v1.3/summoner/by-name/' + summonerName +'?api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
        summoner = requests.get(url)
        print("1 call- Summoner Name Request")
        return addSummonerHelper(summoner, summonerName)
    else:
        print("SummonerName " + summonerName + "has already been added!")
        return

    

def addSummonerId(summonerId):
    if(type(summonerId) is list):
        summonerIds = ','.join(summonerId)
        url = 'https://prod.api.pvp.net/api/lol/na/v1.3/summoner/' + summonerIds + '?api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
        try:
            summoner = requests.get(url).json()
        except(ValueError):
            print(url)
            print(summonerId)
            print("VALUE ERROR, PROBABLY NO JSON THERE")
            return
        print("1 call- SummonerId List Request")
        print("5 second pause...")
        time.sleep(5)
        
        conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
        cursor = conn.cursor()
        
        for i in range(len(summonerId)):
            row = cursor.execute('SELECT summonerId from tblSummoners WHERE summonerId=?', summonerId[i]).fetchone()
            if(row == None):
                name = summoner[summonerId[i]]
                addSummonerHelper(name, summonerId[i])
        return 
        
    else:
        conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
        cursor = conn.cursor()
        row = cursor.execute('SELECT summonerName from tblSummoners WHERE summonerId=?', summonerId).fetchone()
        if(row == None):
            url = 'https://prod.api.pvp.net/api/lol/na/v1.3/summoner/' + summonerId + '?api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
            summoner = requests.get(url)
            print("1 call- SummonerId Request")
            return addSummonerHelper(summoner, summonerId)
        else:
            
            print("SummonerId for " + row.summonerName + " has already been added!")
            return(150)
    
    
def addSummonerHelper(summonerObj, nameId):  
        try:
            if(summonerObj.status_code != 200):
                print("Summoner get error: " + status_codes(summonerObj.status_code))
                return "error"
        except(AttributeError):
            pass
        if(isinstance(summonerObj, requests.Response)):
            summoner = summonerObj.json()
            summoner = summoner[nameId]
        else:
            summoner = summonerObj
        summonerName = summoner['name'].lower()
        ID = str(summoner['id'])
        profileIcon = str(summoner['profileIconId'])
        summonerLevel = str(summoner['summonerLevel'])
        modifiedDate = str(summoner['revisionDate']*1000)
        conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO tblSummoners (summonerName, summonerId, profileIcon,summonerLevel, modifiedDate) VALUES (?,?,?,?,?)''', summonerName, ID, profileIcon, summonerLevel, modifiedDate)
            try:
                print("Summoner " + summonerName + " has been added!")
            except(UnicodeEncodeError):
                pass
        except pyodbc.IntegrityError:
            return
        conn.commit()
        return ID


def getSummonerID(summonerName):
    
    summonerName = summonerName.lower()
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor() 
    row = cursor.execute("select summonerName from tblSummoners where summonerName=?",summonerName).fetchone() 
    if((row) != None):
        """THIS IS NEEDED EVEN THOUGH IT LOOKS SIMILAR ITS FOR ID NOT NAME"""
        row = cursor.execute("select summonerId from tblSummoners where summonerName=?", summonerName).fetchone()
        return(row.summonerId)  
    else:
        ID = addSummonerName(summonerName)
        if(ID == 'error'):
            return 
        else:
            return getSummonerID(summonerName)
              
def getRecentGames(summonerId, isIdBool, addSummonersBool):
    
    """This is used incase a summonerName is provided instead of a summonerId. isId is true if an Id is provided"""
    if(isIdBool == True): 
        ID = str(summonerId)
    else:
        ID = str(getSummonerID(summonerId))
    
    if(ID == None):
        return "That summoner name does not exist"
    
    url = 'https://prod.api.pvp.net/api/lol/na/v1.3/game/by-summoner/'+ ID + '/recent?api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
    games = requests.get(url).json() 
    print("1 call- Games Request")  
    games = games['games']
    
    for i in range(len(games)):
        conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
        cursor = conn.cursor()
        
        current = games[i]
        stats = games[i]['stats']
        
        gameId = str(current['gameId'])
        summonerId = ID
        
        row = cursor.execute("select gameId, summonerId from tblGameItems where gameId=? AND summonerId=?", gameId, summonerId ).fetchone()
        if(row == None):
            
            championId = str(current['championId'])
            createDate = str(current['createDate'])
            gameMode = str(current['gameMode'])
            gameType = str(current['gameType'])
            mapId = str(current['mapId'])
            spell1 = str(current['spell1'])
            spell2 = str(current['spell2'])
            gameSubType = str(current['subType'])
            teamId = str(stats['team'])
            try:
                championsKilled = str(stats['championsKilled'])
            except KeyError:
                championsKilled = '0'           
            try:
                numDeaths = str(stats['numDeaths'])
            except KeyError:
                numDeaths = '0'
            try:
                assists = str(stats['assists'])
            except KeyError: 
                assists = '0'
            goldEarned = str(stats['goldEarned'])
            try:
                creepScore = str(stats['minionsKilled'])
            except:
                creepScore = '0'
                   
            win = str(stats['win'])
            
            try:
                cursor.execute('INSERT INTO tblGames(gameId, summonerId, championId, createDate, gameMode, gameType, mapId, spell1, spell2, gameSubType, teamId, championsKilled, numDeaths, assists, goldEarned, creepScore, win) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',gameId, summonerId, championId, createDate, gameMode, gameType, mapId, spell1, spell2, gameSubType, teamId, championsKilled, numDeaths, assists, goldEarned, creepScore, win)
            except(pyodbc.IntegrityError):
                pass    
      
            try:
                players = games[i]['fellowPlayers']
            except(KeyError):
                players = []

            playersListId = []
            
            for i in range(len(players)):
                try:
                    currentPlayer = players[i]
                    playerChampionId = str(currentPlayer['championId'])
                    playerSummonerId = str(currentPlayer['summonerId'])
                    playerTeamId = str(currentPlayer['teamId'])
                    cursor.execute('INSERT INTO tblSummonersPlayedWith(gameId, summonerId, otherPlayerId, summonerTeam, otherPlayerTeam, otherPlayerChampion) VALUES(?,?,?,?,?,?)',gameId, summonerId, playerSummonerId, teamId, playerTeamId, playerChampionId)
                    conn.commit()
                    playersListId.append(playerSummonerId)
                except:
                    pass
            
            if(addSummonersBool == True):
                addSummonerId(playersListId)
            
            try:   
                item = str(stats['item0'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "0")
                conn.commit()
            except KeyError:
                pass
            try:
                item = str(stats['item1'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "1")
                conn.commit()
            except KeyError:
                pass
            try:
                item = str(stats['item2'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "2")
                conn.commit()
            except KeyError:
                pass
            try:
                item = str(stats['item3'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "3")
                conn.commit()
            except KeyError:
                pass
            try:
                item = str(stats['item4'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "4")
                conn.commit()
            except KeyError:
                pass
            try:
                item = str(stats['item5'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "5")
                conn.commit()
            except KeyError:
                pass
            try:
                item = str(stats['item6'])
                cursor.execute('INSERT INTO tblGameItems(gameId, summonerId, itemId, itemSlot)VALUES (?,?,?,?)', gameId, summonerId, item, "6")
                conn.commit()
            except KeyError:
                pass
            
        else:
            print('This game has already been entered. GameId: '+ gameId)
             
def status_codes(code):
    if(code == 400):
        return "Bad Request"  
    elif(code == 401):
        return "Unauthorized"
    elif(code ==404):
        return "Summoner Not Found"
    elif(code ==500):
        return "Internal Server Error"
    elif(code ==503):
        return "Service Unavaliable"
    else:
        return "Unspecified Error Code "+str(code)
      
"""Adds missing champions to the champions table in the database"""    
def addChampions():
    url = 'https://prod.api.pvp.net/api/lol/na/v1.1/champion?api_key=8b1b544f-26c1-4309-98fb-8e2e2afd3939'
    champions = requests.get(url).json()
    print("1 call- Champions Request")
    champions = champions['champions']
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor()
    for i in range(len(champions)):
        current = champions[i]
        ID = str(current['id'])
        row = cursor.execute("select championId from tblChampions where championId=?",ID).fetchone() 
        name = str(current['name'])
        if(row == None):
            cursor.execute('''INSERT INTO tblChampions(championId, championName) VALUES (?,?)''', ID,name)
            print(name + " has been added to the database!")
        else:
            pass
            
    conn.commit()    

def collectAllRecentGames(addSummonersBool):
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor()
    row = cursor.execute("select summonerId from tblSummoners").fetchall()
    count = 0
    for i in range(len(row)):
        Id = (row[i].summonerId)
        getRecentGames(Id, True, addSummonersBool)
        if (i % 8 == 0):
            print("10 second pause...")
            time.sleep(10)
        count = count + 1
        print("Summoners done: " + str(count))
        conn.commit()
    
def addItems():
    url = 'http://prod.api.pvp.net/api/lol/static-data/na/v1.1/item?itemListData=all&api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
    items = requests.get(url).json()
    print("1 call- Items Request")
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor()
    for i in range(4000):
        try:
            name = items['data'][str(i)]['name']
            itemId = str(i)
            description = items['data'][str(i)]['plaintext']
            row = cursor.execute("select itemId from tblItems where itemId=?",itemId).fetchone()
            if(row == None):    
                cursor.execute('INSERT INTO tblItems(itemId, itemName, description) VALUES (?,?,?)', itemId, name, description)
                conn.commit()
        except(KeyError):
            pass

def updateChallengers():
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor()
    tblExport.tblExporter('tblChallengers')
    cursor.execute("delete from tblChallengers")
    conn.commit()
    url = 'https://prod.api.pvp.net/api/lol/na/v2.3/league/challenger?type=RANKED_SOLO_5x5&api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
    challengers = requests.get(url).json()
    challengers = challengers['entries']
    for i in range(len(challengers)):
        challenger = challengers[i]
        playerId = str(challenger['playerOrTeamId'])
        if(addSummonerId(playerId) == 150):
            pass
        else:   
            print("1.5 second pause...")         
            time.sleep(1.5)
        leaguePoints = str(challenger['leaguePoints'])
        wins = str(challenger['wins'])
        cursor.execute('insert into tblChallengers(playerId, leaguePoints, wins) values(?,?,?)', playerId, leaguePoints, wins)
        conn.commit()
