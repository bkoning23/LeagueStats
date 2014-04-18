'''
Created on Apr 3, 2014

@author: Brendan
'''

import pyodbc
import requests
import addSummonerHelper
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