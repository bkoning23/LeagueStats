'''
Created on Apr 3, 2014

@author: Brendan
'''
from LeagueDatabase import collectAllRecentGames
import time


start_time = time.time()
collectAllRecentGames(True)
print (time.time() - start_time, "seconds")

input("Press enter to close")