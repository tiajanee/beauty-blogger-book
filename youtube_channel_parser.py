from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import re
import pandas as pd
import csv


#JAMES_CHARLES = 'UCucot-Zp428OwkyRm2I7v2Q'

PONY_SYNDROME = 'UCT-_4GqC-yLY1xtTHhwY0hA'
JAMES_CHARLES = 'UCucot-Zp428OwkyRm2I7v2Q'
NYMA_TANG = 'UCroDJPcFCf6DBmHns6Xeb8g'
ALYSSA_FOREVER = 'UCNEwha2SIAz3NTtv9G0QPsg'
JASMINE_BROWN = 'UCw95JvOs39snnMPkYs-6Sog'


#25 youtube handles of bloggers that are white/white-passing (based on my perception)
WP_YOUTUBER_NAMES = ['jeffreestar', 'Jaclynhill1', 'macbby11', 'nikkietutorials', 'laura88lee', 'pixiwoo', 'kandeejohnson', 'zoella280390', 'makeupgeektv', 'stilaBabe09', 
'shaaanxo', 'ChloeMorello', 'Laurenbeautyy', 'Missglamorazzi', 'AllThatGlitters21', 'Juicystar07', 'MannyMua733', 'GlamLifeGuru', 'CutiePieMarzia', 'KathleenLights',
'pixi2woo', 'CarliBel55', JAMES_CHARLES, 'HauteBrilliance', 'SierraMarieMakeup']

#25 youtube handles og bloggers that are disenfranchised in beauty community/darker skinned (based on my perception)
DK_YOUTUBER_NAMES = ['iamkareno', 'theepatrickstarrr', 'wwwengie', 'bubzbeauty', 'itsalissaweekly', 'mylifeaseva', 'Dope2111', PONY_SYNDROME, 'MichellePhan', 'itsmyRayeRaye', 
'BritPopPrincess', 'DulceCandy87', 'AndreasChoice', 'macbarbie07', 'ThatsHeart', 'SmartistaBeauty', NYMA_TANG, 'beautycrush', ALYSSA_FOREVER, JASMINE_BROWN, 'Cydbeats', 
'Irishcel507', 'clothesencounters', 'TTLYTEALA', 'makeupbytinayong']


def main():
    names = WP_YOUTUBER_NAMES
    #full list of YT users
    #names = WP_YOUTUBER_NAMES + DK_YOUTUBER_NAMES
    for name in names:
        create_channel_url(name)
        get_youtube_videos(name)
        create_write_csv(name)



def create_channel_url(name):
    #debugged, works, need to add comments
    try:
        youtube = "https://www.youtube.com/user/{}/videos?sort=p&view=0&flow=grid".format(name)
        attempt = urlopen(youtube)

    except HTTPError:
        youtube = "https://www.youtube.com/channel/{}/videos?sort=p&view=0&flow=grid".format(name)
        print(name)
        attempt = urlopen(youtube)
    
    return youtube


    

def get_youtube_videos(name):
    #debugged works, need to add comments
    youtube = create_channel_url(name)
    page = urlopen(youtube).read()
    soup = BeautifulSoup(page,'html.parser')
    soup.prettify()
    #initialize empty list of links
    links = []

    #pulls links that belong to a particular class
    results = soup.find_all('a',{'class':'yt-uix-sessionlink'})
    for link in results:
        # find the url
        url = link.get("href")
    
        #deletes links that are not channel video links
        if "/watch?v=" not in url:
            continue
        else:
            #add url link to list of links 
            links.append(url)
    return links

def create_write_csv(name):
    links = get_youtube_videos(name)
    with open('wp_youtubers.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['channel_name', 'youtube_url'])
            index = 1
            print(name)
            for index in range(11):
                row_link =  links[index]
                filewriter.writerow([name, row_link])



    #print(links)

if __name__ == "__main__":
    main()
    