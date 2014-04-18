'''
Created on Apr 3, 2014

@author: Brendan
'''

import time
import requests
import pyodbc
import addSummonerHelper

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
        time.sleep(5)
        print("5 second pause...")
        
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
        row = cursor.execute('SELECT summonerId from tblSummoners WHERE summonerId=?', summonerId).fetchone()
        if(row == None):
            url = 'https://prod.api.pvp.net/api/lol/na/v1.3/summoner/' + summonerId + '?api_key=ec23e4b8-9674-4c38-8904-861ef246aa2b'
            summoner = requests.get(url)
            print("1 call- SummonerId Request")
            return addSummonerHelper(summoner, summonerId)
        else:
            print("SummonerId " + summonerId + " has already been added!")
            return
    
    