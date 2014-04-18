'''
Created on Apr 3, 2014

@author: Brendan
'''

from LeagueDatabase import getRecentGames

name = input('Summoner Name: ')

getRecentGames(name, False, False)

input("Push enter to close")
