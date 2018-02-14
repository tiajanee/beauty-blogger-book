from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import re
import csv
import glob



PONY_SYNDROME = 'UCT-_4GqC-yLY1xtTHhwY0hA'
JAMES_CHARLES = 'UCucot-Zp428OwkyRm2I7v2Q'
NYMA_TANG = 'UCroDJPcFCf6DBmHns6Xeb8g'
ALYSSA_FOREVER = 'UCNEwha2SIAz3NTtv9G0QPsg'
JASMINE_BROWN = 'UCw95JvOs39snnMPkYs-6Sog'


#25 youtube handles of bloggers that are white/white-passing (based on my perception)
WP_YOUTUBER_NAMES = [
	'jeffreestar', 'Jaclynhill1', 'macbby11', 'nikkietutorials', 'laura88lee', 
	'pixiwoo', 'kandeejohnson', 'zoella280390', 'makeupgeektv', 'stilaBabe09', 
	'shaaanxo', 'ChloeMorello', 'Laurenbeautyy', 'Missglamorazzi', 'AllThatGlitters21', 
	'Juicystar07', 'MannyMua733', 'GlamLifeGuru', 'CutiePieMarzia', 'KathleenLights',
	'pixi2woo', 'CarliBel55', JAMES_CHARLES, 'HauteBrilliance', 'SierraMarieMakeup'
]

#25 youtube handles og bloggers that are disenfranchised in beauty community/darker skinned (based on my perception)
DK_YOUTUBER_NAMES = [
	'iamkareno', 'theepatrickstarrr', 'wwwengie', 'bubzbeauty', 
	'itsalissaweekly', 'mylifeaseva', 'Dope2111', PONY_SYNDROME, 'MichellePhan', 'itsmyRayeRaye', 
	'BritPopPrincess', 'DulceCandy87', 'AndreasChoice', 'macbarbie07', 'ThatsHeart', 
	'SmartistaBeauty', NYMA_TANG, 'beautycrush', ALYSSA_FOREVER, JASMINE_BROWN, 'Cydbeats', 
	'Irishcel507', 'clothesencounters', 'TTLYTEALA', 'makeupbytinayong'
]

# YOUTUBE URLS
URL = "https://www.youtube.com/"
CHANNEL = "channel/"
USER = "user/"
REF = "/videos?sort=p&view=0&flow=grid"

# DATASETS
DATA_FILE_PATH = "/datasets"
DATASETS = [
	"wp.csv",
	"dp.csv",
	"all.csv",
	"WP/",
	"DP/",
]


def _FILE_PATH(name):
	""" Create url from name """
	if name[0] is "U":
		return URL + CHANNEL + name + REF 
	else:
		return URL + USER + name + REF

