'''
Created on Apr 3, 2014

@author: Brendan
'''
from LeagueDatabase import getRecentGames

priority = ['cookieking23', 'ultra25','eragon7651','boilerup23']

for i in range(len(priority)):
    getRecentGames(priority[i],False,False)
    print(str(priority[i]) + ' has been updated!')
input('Push Enter to Close')
    