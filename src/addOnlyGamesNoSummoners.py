'''
Created on Apr 3, 2014

@author: Brendan
'''
from LeagueDatabase import collectAllRecentGames
import time

start_time = time.time()
collectAllRecentGames(False)
print (time.time() - start_time, "seconds")


input('Push Enter to Close')

