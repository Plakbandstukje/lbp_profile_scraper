from bs4 import BeautifulSoup
from urllib2 import urlopen

import sys
import time



def findSessionPlayers(sessionurl):
    players = []
    
    # prepare soup
    soupdata = urlopen(sessionurl).read()
    soup = BeautifulSoup(soupdata)
    
    # find players in session
    plist = soup.find('div', attrs = {'class': 'sidebar'}).find('table').find_all('tr')
    for pentry in plist:
        player = pentry.find_all('a')[1].getText()
        players.append(player)
 
    return players
    


def findPlayerData(player):
    playerdata = {
        'name': '',
        'profile': '',
        'authorcount': 0,
        'heartcount': 0,
        'playcount': 0,
        'mostplayed': '',
        'levels': []
    }
    
    
    # prepare soup
    soupurl = 'http://lbp.me/u/' + player + '/levels'
    soupdata = urlopen(soupurl).read()
    soup = BeautifulSoup(soupdata) 
    
    # set name and profile
    playerdata['name'] = player
    playerdata['profile'] = 'http://lbp.me/u/' + player
    
    # set author heart count
    authorcount = soup.find('div', class_='user-profile-details')
    authorcount = authorcount.find('li', class_='hearted')
    authorcount = authorcount.getText().replace(",", "")
    playerdata['authorcount'] = int(authorcount)
    
    # the rest
    llist = soup.find_all('li', class_='level')
    for lentry in llist:
        # set level url
        level = lentry.find_all('a')[1].get('href')
        level = 'http://lbp.me' + level
        playerdata['levels'].append(level)
        
        # set heartcount
        heartcount = lentry.find('li', class_='hearted').getText()
        heartcount = heartcount.replace(",", "")
        playerdata['heartcount'] += int(heartcount)
        
        # set highest played level
        playcount = lentry.find('li', class_='plays').getText()
        playcount = int(playcount.replace(",", ""))
        if playcount >= playerdata['playcount']:
            playerdata['playcount'] = playcount
            playerdata['mostplayed'] = level
    
    return playerdata;



def run():
    authorlist = []
    levellist = []
    playlist = []
    
    if len(sys.argv) != 2:
        print "Invalid arguments."
        return 0;
        
    
    players = findSessionPlayers(sys.argv[1])
    
    for player in players:
        d = findPlayerData(player)
        
        if d['authorcount'] < 30:
            print "adding " + d['name'] + " to author list ..."
            authorlist.append(d['profile'])
        else:
            print "skipping " + d['name'] + ". Already enough author hearts."
        
        if d['heartcount'] < 50:
            print "adding levels by " + d['name'] + " to level list ..."
            max = min(50 - d['heartcount'], 6)
            levellist.extend(d['levels'][:max])
        else:
            print "skipping " + d['name'] + ". Already enough level hearts."
        
        if d['playcount'] < 50:
            print "adding most played level by " + d['name'] + " to play list ..."
            playlist.append(d['mostplayed'])
        else:
            print "skipping " + d['name'] + ". Already enough plays"
        
        print "Waiting ..."
        time.sleep(2)

    print "Writing lists to urls.txt ..."
    f = open("urls.txt", "w")
    
    f.write("Like these authors:\n\n")
    for a in authorlist:
        f.write(a + "\n")
        
    f.write("\n\n\nAdd these levels to your queue and heart them in-game:\n\n")
    for l in levellist:
        f.write(l + "\n")
        
    f.write("\n\n\nPlay these levels:\n\n")
    for p in playlist:
        f.write(p + "\n")
            
    print "Done."
    f.close()
                

        
        
        
run()