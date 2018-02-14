from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random

# list of all user names: done
# interpolate the channel name into most popular url
# scrape for titles of videos/urls: done
# go to each link and do this VVVVVV


#making aliases for youtubers whose user channel ids are hash looking strings
PONY_SYNDROME = 'UCT-_4GqC-yLY1xtTHhwY0hA'
JAMES_CHARLES = 'UCucot-Zp428OwkyRm2I7v2Q'
NYMA_TANG = 'UCroDJPcFCf6DBmHns6Xeb8g'
ALYSSA_FOREVER = 'UCNEwha2SIAz3NTtv9G0QPsg'
JASMINE_BROWN = 'UCw95JvOs39snnMPkYs-6Sog'


#25 youtube handles of bloggers that are white/white-passing (based on my perception)
WP_YOUTUBER_NAMES = ['jeffreystar', 'jaclynhill', 'macbby11', 'nikkietutorials', 'laura88lee', 'pixiwoo', 'kandeejohnson', 'zoella280390', 'makeupgeektv', 'stilaBabe09', 
'shaaanxo', 'ChloeMorello', 'Laurenbeautyy', 'Missglamorazzi', 'AllThatGlitters21', 'Juicystar07', 'MannyMua733', 'GlamLifeGuru', 'CutiePieMarzia', 'Kathleen Lights',
'pixi2woo', 'CarliBel55', JAMES_CHARLES, 'HauteBrilliance', 'SierraMarieMakeup']

#25 youtube handles og bloggers that are disenfranchised in beauty community/darker skinned (based on my perception)
DK_YOUTUBER_NAMES = ['iamkareno', 'theepatrickstarrr', 'wwwengie', 'bubzbeauty', 'itsalissaweekly', 'mylifeaseva', 'Dope2111', PONY_SYNDROME, 'MichellePhan', 'itsmyRayeRaye', 
'BritPopPrincess', 'DulceCandy87', 'AndreasChoice', 'macbarbie07', 'ThatsHeart', 'SmartistaBeauty', NYMA_TANG, 'beautycrush', ALYSSA_FOREVER, JASMINE_BROWN, 'Cydbeats', 
'Irishcel507', 'clothesencounters', 'TTLYTEALA', 'makeupbytinayong']

# for testing
SAMPLE_YOUTUBE_NAMES = []

for _ in range(0, 10):
	SAMPLE_YOUTUBE_NAMES.append(random.choice(DK_YOUTUBER_NAMES + WP_YOUTUBER_NAMES))

print(SAMPLE_YOUTUBE_NAMES)

#INDIVIDUAL YOUTUBE LINK PARSING

youtube_path = "https://www.youtube.com/watch?time_continue=1&v=IlCmIBMPhp8" 
page = urlopen(youtube_path)
soup = BeautifulSoup(page, 'lxml')
soup.prettify()
#parses through webpage and cleans data to find view count of video
un_views_count = str(soup.find('div', class_="watch-view-count"))
views_count = re.sub('[^0-9]','', un_views_count)
views_count = re.sub(',', '', views_count)

#parses through webpage and cleans data to get dislike counts
un_dislike_count = str(soup.find('button', title="I dislike this", type="button"))
dislike_count =  re.sub('[^0-9,]',' ', un_dislike_count)
dislike_count = re.sub(',', '', dislike_count).split()
del dislike_count[1]


#parses through webpage and cleans data to get likes counts
un_likes_amount = str(soup.find('button', title="I like this", type='button'))
likes_count =  re.sub('[^0-9,]',' ', un_likes_amount)
likes_count = re.sub(',', '', likes_count).split()
del likes_count[1]

print("dislikes:", int(dislike_count[0]))
print("likes:", int(likes_count[0]))
print('views:', views_count)
# print(len(WP_YOUTUBER_NAMES))
# print(len(DK_YOUTUBER_NAMES))

