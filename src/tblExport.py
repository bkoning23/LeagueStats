'''
Created on Apr 3, 2014

@author: Brendan Koning
'''

import pyodbc, csv, datetime

def tblExporter(table):
    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\Brendan\\Dropbox\\LeagueDB\\League.accdb")
    cursor = conn.cursor()
    
    
    rows = cursor.execute('select * from tblChallengers ORDER BY leaguePoints DESC').fetchall()

    
    date = str(datetime.date.today())
    location = 'C:\\Users\\Brendan\\Desktop\\ChallengerTXT\\' +date+'.txt'
    print(location)
    outputFile = open(location, 'w')
    datawriter = csv.writer(outputFile)
    datawriter.writerows(rows)
    outputFile.close()
    