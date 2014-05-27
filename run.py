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
    plist = soup.find('div', class_='sidebar').find('table').find_all('tr')
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
        
        # is playcount on lbp.me in unique players?
        if d['playcount'] < 60 and d['mostplayed'] != "":
            print "adding most played level by " + d['name'] + " to play list ..."
            playlist.append(d['mostplayed'])
        else:
            print "skipping " + d['name'] + ". Already enough plays or no public profile."
        
        print "Waiting ..."
        time.sleep(2)

    print "Writing lists to lbp.html ..."
    f = open("lbp.html", "w")
    f.write("""
        <html>
            <head>
                <title>LBP</title>    
            </head>
            <body>
    """)
    
    f.write("<p>Like these authors:</p>")
    for a in authorlist:
        f.write("<a href='" + a + "'>" + a + "</a></br>")
        
    f.write("<p>Add these levels to your queue and heart them in-game:</p>")
    for l in levellist:
        f.write("<a href='" + l + "'>" + l + "</a></br>")
        
    f.write("<p>Play these levels:</p>")
    for p in playlist:
        f.write("<a href='" + p + "'>" + p + "</a></br>")
            
    f.write("""
            <p><a href='https://github.com/mmans93/lbp_psnprofiles'>source</a></p>
            </body>
        </html>
    """)
    
    print "Done."
    f.close()
                

        
        
        
run()