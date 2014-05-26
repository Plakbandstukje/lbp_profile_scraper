from bs4 import BeautifulSoup
from urllib2 import urlopen

import sys

def findLbpLevel(player):
    lbpurl = ""
    lbphearts = 0;
    
    soupurl = "http://lbp.me/u/" + player + "/levels"
    soupdata = urlopen(soupurl).read()
    #soupdata = open('lbpme.html').read()
    soup = BeautifulSoup(soupdata)
    levellist = soup.find_all('li', attrs = {'class': 'level'})
    for levelentry in levellist:
        hearts = levelentry.find('li', attrs = {'class': 'hearted'}).getText()
        
        if len(hearts) > 2:
            return ""

        hearts = int(hearts)
        if hearts > lbphearts:
            lbpurl = "http://lbp.me" + levelentry.find_all('a')[1].get('href')
            
    return lbpurl

def findSessionMembers(url):
    members = []
     
    soupdata = urlopen(url).read()
    #soupdata = open('psnprofiles.html').read()
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
        
    players = findSessionMembers(sessionurl)
    for player in players:
        print findLbpLevel(player)

run()