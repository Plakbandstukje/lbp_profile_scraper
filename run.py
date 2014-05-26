from bs4 import BeautifulSoup
from urllib2 import urlopen

import sys
import time

def findLbpLevels(player):
    levels = []
    
    soupurl = "http://lbp.me/u/" + player + "/levels"
    soupdata = urlopen(soupurl).read()
    soup = BeautifulSoup(soupdata)
    
    levellist = soup.find_all('li', attrs = {'class': 'level'})
    
    for levelentry in levellist:
        hearts = levelentry.find('li', attrs = {'class': 'hearted'}).getText()
        
        if len(hearts) > 2:
            return []

        hearts = int(hearts)
        if hearts > 49:
            return []
            
        level = levelentry.find_all('a')[1].get('href')
        levels.append(level)
            
    return levels

def findSessionMembers(url):
    members = []
     
    soupdata = urlopen(url).read()
    soup = BeautifulSoup(soupdata)
    
    playerlist = soup.find('div', attrs = {'class': 'sidebar'}).find('table').find_all('tr')
   
    for playerentry in playerlist:
        player = playerentry.find_all('td')[1].find('a').getText()
        members.append(player)
        
    return members
        
    
def run():
    if len(sys.argv) == 1:
        print "No session given. "
        return 0;    
        
    sessionurl = sys.argv[1]
    if sessionurl[:39] != "http://psnprofiles.com/gaming-sessions/":
        print "Wrong session url. "
        return 0;
        
    print "Finding players ..."
    players = findSessionMembers(sessionurl)
    
    print "Finding levels ..."
    levels = []
    for player in players:
        print "Finding levels for player " + player + " ..."
        playerlevels = findLbpLevels(player)
        levels.extend(playerlevels)
        print "Waiting ..."
        time.sleep(2)
        
    print "Writing URLs to urls.txt"
    f = open("urls.txt", "w")
    for player in players:
        f.write("http://lbp.me/u/" + player + "\n")    
    f.write("\n")
    for level in levels:
        f.write("http://lbp.me" + level + "\n")
    f.close()
    
    print "Done."
    
    

run()