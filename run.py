from bs4 import BeautifulSoup
from urllib2 import urlopen

import sys
import time
import datetime



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
        
        if d['playcount'] < 50 and d['mostplayed'] != "":
            print "adding most played level by " + d['name'] + " to play list ..."
            playlist.append(d['mostplayed'])
        else:
            print "skipping " + d['name'] + ". Already enough plays or no public profile."
        
        print "Waiting ..."
        time.sleep(2)

    
    html_begin = "<html><head><title>LBP</title><link rel='stylesheet' ' href='style.css' type='text/css' /></head><body><table><tr>"
    update_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    html_end = "</tr></table><p>Last updated: " + update_time + "</p></body></html>"
    
    f = open("list.html", "w")
    f.write(html_begin)
    
    print "Writing authors list ..."
    f.write("<td><p>Like these authors on lbp.me:</p>\n")
    for a in authorlist:
        f.write("<a href='" + a + "' target='_blank'>" + a + "</a></br>\n")
    f.write("</td>")
    
    print "Writing levels list ..."
    f.write("<td><p>Add these levels to your queue and heart them in-game:</p>\n")
    for l in levellist:
        f.write("<a href='" + l + "' target='_blank'>" + l + "</a></br>\n")
    f.write("</td>")
        
    print "Writing plays list ..."
    f.write("<td><p>Add these levels to your queue and play them in-game:</p>\n")
    for p in playlist:
        f.write("<a href='" + p + "' target='_blank'>" + p + "</a></br>\n")
    f.write("</td>" + html_end)
    f.close()
    
    
    print "Done."
        
run()