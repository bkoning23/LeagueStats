'''
Created on Apr 3, 2014

@author: Brendan
'''

import requests
import pyodbc

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