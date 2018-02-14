import re
import csv
import glob
import pprint
import httplib2
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, SoupStrainer

PONY_SYNDROME = 'UCT-_4GqC-yLY1xtTHhwY0hA'
JAMES_CHARLES = 'UCucot-Zp428OwkyRm2I7v2Q'
NYMA_TANG = 'UCroDJPcFCf6DBmHns6Xeb8g'
ALYSSA_FOREVER = 'UCNEwha2SIAz3NTtv9G0QPsg'
JASMINE_BROWN = 'UCw95JvOs39snnMPkYs-6Sog'


# 25 youtube handles of bloggers that are white/white-passing (based on my perception)
WP_YOUTUBER_NAMES = [
	'jeffreestar', 'Jaclynhill1', 'macbby11', 'nikkietutorials', 'laura88lee', 
	'pixiwoo', 'kandeejohnson', 'zoella280390', 'makeupgeektv', 'stilaBabe09', 
	'shaaanxo', 'ChloeMorello', 'Laurenbeautyy', 'Missglamorazzi', 'AllThatGlitters21', 
	'Juicystar07', 'MannyMua733', 'GlamLifeGuru', 'CutiePieMarzia', 'KathleenLights',
	'pixi2woo', 'CarliBel55', JAMES_CHARLES, 'HauteBrilliance', 'SierraMarieMakeup'
]

# 25 youtube handles og bloggers that are disenfranchised in beauty community/darker skinned (based on my perception)
DK_YOUTUBER_NAMES = [
	'iamkareno', 'theepatrickstarrr', 'wwwengie', 'bubzbeauty', 
	'itsalissaweekly', 'mylifeaseva', 'Dope2111', PONY_SYNDROME, 'MichellePhan', 'itsmyRayeRaye', 
	'BritPopPrincess', 'DulceCandy87', 'AndreasChoice', 'macbarbie07', 'ThatsHeart', 
	'SmartistaBeauty', NYMA_TANG, 'beautycrush', ALYSSA_FOREVER, JASMINE_BROWN, 'Cydbeats', 
	'Irishcel507', 'clothesencounters', 'TTLYTEALA', 'makeupbytinayong'
]

# YOUTUBE URLS
URL = "https://www.youtube.com"

#NOTE: some channel pages contain either a link with a channel path OR a user path, dependent on the channel

CHANNEL = "/channel/"
USER = "/user/"

#orders videos in descending order of popularity
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

def main():

	#create_datasets(DATASETS)

	# specify list
	names = DK_YOUTUBER_NAMES[:2]   #+ WP_YOUTUBER_NAMES
	for name in names:
		
		# get top ten video links
		
		url = _url(name)
		scraper = scrape_top_videos(url)
		top_10 = get_top_10(url)
		pprint.pprint(top_10)
		
		all_atts = []

		for link in top_10:
			link = URL + link #should have been 10 user video links, might be more?
			all_atts.append(get_attributes(link)) #was saving like a variable instead of a list, test this
		
		youtuber = create_youtuber_csv(name, all_atts)

		# #	combine the datasets in WK/DP
		# insert_in_hue_dataset(youtuber)

		# #combine the datasets in all
		# insert_in_all_dataset(youtuber, url(name))


def scrape_top_videos(name):
	'''
	gets all embedded video links in user's channel, appended in desc popularity

	'''


	#reads in HTML to parse
	page = urlopen(name).read()
	soup = BeautifulSoup(page,'html.parser')
	soup.prettify()
    
    #initialize empty list of to be filled with all non-unique links;
    #after parsing though the class, we retrieve repeat links
	repeat_links = []

	
	#locates where embedded links to videos are stored
	results = soup.find_all('a',{'class':'yt-uix-sessionlink'})

	for link in results:

		#retrieves url from specific class
		url = link.get("href")

		#some links aren't video links, here we ignore them
		if "/watch?v=" not in url:
			continue

		#appends url to list of repeat_links to later be cleaned
		else:
			#for index in range(11):
			repeat_links.append(url)
	
	#gets rid of all repeat links retreived from channel page
	unique_links = repeat_links[::2]

	return unique_links


def _url(name):
	'''
	Create url from name 

	'''

	#debugged
	if name[0] is "U":
		url = URL + CHANNEL + name + REF 
	else:
		url = URL + USER + name + REF
	return url


def get_top_10(name):
	'''
	get top 10 most popular videos for each name

 	'''
	
	#the bug might be catalized here, maybe the links I scraped weren't all user video links
	popular_vid_links = scrape_top_videos(name)
	index = 0
	ten_links = []
	for index in range(10):
		ten_links.append(popular_vid_links[index])
		index =  index + 1 
	return ten_links

def get_attributes(name):

	#bug: scraping links of related videos for views of video link instead of links provided in list
	links = get_top_10(name)

	#empty list created to hold list of video attributes(views, likes, dislikes)
	all_atts = []

	for link in links:
		print(link)
		youtube_path = URL + link
		all_atts.append(youtube_path)
		web_page = urlopen(youtube_path)
		video_soup = BeautifulSoup(web_page, 'lxml')
		video_soup.prettify()
		
		#parses through webpage and cleans data to find view count of video
		spans = video_soup.find_all('span', {'class' : "view-count style-scope yt-view-count-renderer"})
		print(spans)

		#takes only the text in the span element
		lines = [span.get_text() for span in spans]
		print(lines)

		#cleaning the text of symbols and integers
		dirty_views_count = re.sub('[^0-9]','', lines)
		print(dirty_views_count)

		#returns a double count, gets rid of the repeat amount
		clean_views_count = re.sub(',', '', dirty_views_count)
		print(clean_views_count)
		all_atts.append(clean_views_count)

	return all_atts


	# 	#parses through webpage and cleans data to get likes counts
	# 	un_likes_amount = str(soup.find('button', title="I like this", type='button'))
	# 	likes_count =  re.sub('[^0-9,]',' ', un_likes_amount)
	# 	likes_count = re.sub(',', '', likes_count).split()
	# 	all_atts.append(likes_count)
	

	# 	#parses through webpage and cleans data to get dislike counts
	# 	un_dislike_count = str(soup.find('button', title="I dislike this", type="button"))
	# 	dislike_count =  re.sub('[^0-9,]',' ', un_dislike_count)
	# 	dislike_count = re.sub(',', '', dislike_count).split()
	# 	all_atts.append(dislike_count)


	# return all_atts

def create_user_csv(name, all_atts):
	#might not need to call this since i append to an empty list with all attributes in main
	all_atts = get_attributes(name) 

	
	with open('{}.csv', 'a').format(name) as csvfile:
            filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['video_link', 'views', 'likes', 'dislikes'])
            print(name)
          	filewriter.writerow([all_atts])



if __name__ == "__main__":
    main()
















