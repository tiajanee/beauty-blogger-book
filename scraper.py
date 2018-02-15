import re
import csv
import glob
import pprint
import httplib2
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup, SoupStrainer
import os

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
DATA_FILE_PATH = "datasets/"
DATASETS = [
	"wp.csv",
	"dp.csv",
	"all.csv",
	"WP/",
	"DP/",
]

DIR = '/Users/tiaking/Desktop/beauty_blogger-binder'

def main():

	#create_datasets(DATASETS)

	# specify list
	names = DK_YOUTUBER_NAMES[:3] + WP_YOUTUBER_NAMES[:3]
	for name in names:
		
		
		url = _url(name)
		scraper = scrape_top_videos(url)
		top_10 = get_top_10(url)
		full_att_list = get_attributes(url)
		create_youtuber_csv(url, name, full_att_list)
		insert_in_hue_dataset(name, full_att_list)
		insert_in_all_dataset(name, full_att_list)

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
	
	popular_vid_links = scrape_top_videos(name)
	index = 0
	ten_links = []
	for index in range(10):
		ten_links.append(popular_vid_links[index])
		index =  index + 1
	return ten_links

def get_attributes(name):

# 	#bug: scraping links of related videos for views of video link instead of links provided in list
	videos = get_top_10(name)
	#empty list created to hold list of video attributes(views, likes, dislikes)
	all_atts = []
	for video in videos:
		youtuber_list = []
		youtube_path = URL + video
		youtuber_list.append(youtube_path)
		web_page = urlopen(youtube_path)
		video_soup = BeautifulSoup(web_page, 'html.parser')
		pprint.pprint(youtube_path)
		#parses through webpage and cleans data to find view count of video
		try:
			spans = str(video_soup.find('span', attrs={"class":"stat view-count"}))
			views_count = re.sub('[^0-9]','', spans)
			youtuber_list.append(int(views_count))
		except: 
			spans = str(video_soup.find('div', 'watch-view-count'))
			views_count = re.sub('[^0-9]','', spans)
			youtuber_list.append(int(views_count))

		#parses through webpage and cleans data to get likes counts
		un_likes_amount = str(video_soup.find('button', title="I like this", type='button'))
		dirty_likes_count =  re.sub('[^0-9,]',' ', un_likes_amount)
		clean_likes_count = re.sub(',', '', dirty_likes_count).split()[0]

		youtuber_list.append(int(clean_likes_count))
	

 		#parses through webpage and cleans data to get dislike counts

		un_dislike_count = str(video_soup.find('button', title="I dislike this", type="button"))
		dirty_dislike_count =  re.sub('[^0-9,]',' ', un_dislike_count)
		clean_dislike_count = re.sub(',', '', dirty_dislike_count).split()[0]
		youtuber_list.append(int(clean_dislike_count))

		all_atts.append(youtuber_list)

	return all_atts


def create_youtuber_csv(name, user, all_atts):
	#might not need to call this since i append to an empty list with all attributes in main
	all_atts = get_attributes(name) 

	if user in DK_YOUTUBER_NAMES:
		
		file_path = DATA_FILE_PATH + DATASETS[4] + '{}.csv'.format(user)
		
		if not os.path.exists(os.path.dirname(file_path)):
			try:
				os.makedirs(os.path.dirname(file_path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['video_link', 'views', 'likes', 'dislikes'])
			index = 1
			for index in range(len(all_atts)):
				filewriter.writerow(all_atts[index])
				index = index + 1 
	
	if user in WP_YOUTUBER_NAMES:
		
		file_path = DATA_FILE_PATH + DATASETS[3] + '{}.csv'.format(user)
		
		if not os.path.exists(os.path.dirname(file_path)):
			try:
				os.makedirs(os.path.dirname(file_path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['video_link', 'views', 'likes', 'dislikes'])
			index = 1
			for index in range(len(all_atts)):
				filewriter.writerow(all_atts[index])
				index = index + 1 
	return all_atts
	
def insert_in_hue_dataset(user, all_atts):

	if user in DK_YOUTUBER_NAMES:
		file_path = DATA_FILE_PATH + DATASETS[1]

		if not os.path.exists(os.path.dirname(file_path)):
				try:
					os.makedirs(os.path.dirname(file_path))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes'])
			index = 1

			for index in range(len(all_atts)):
				all_atts[index].insert(0, user)
				filewriter.writerow(all_atts[index])
				index = index + 1 
	

	if user in WP_YOUTUBER_NAMES:
		file_path = DATA_FILE_PATH + DATASETS[0]

		if not os.path.exists(os.path.dirname(file_path)):
				try:
					os.makedirs(os.path.dirname(file_path))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes'])
			index = 1

			for index in range(len(all_atts)):
				all_atts[index].insert(0, user)
				filewriter.writerow(all_atts[index])
				index = index + 1 
	
def insert_in_all_dataset(user, all_atts):
	
	if user in DK_YOUTUBER_NAMES:
		file_path = DATA_FILE_PATH + DATASETS[2]

		if not os.path.exists(os.path.dirname(file_path)):
				try:
					os.makedirs(os.path.dirname(file_path))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes', 'type'])
			index = 1


			for index in range(len(all_atts)):
				all_atts[index].append('DK')
				filewriter.writerow(all_atts[index])
				index = index + 1 


	if user in WP_YOUTUBER_NAMES:
		file_path = DATA_FILE_PATH + DATASETS[2]

		if not os.path.exists(os.path.dirname(file_path)):
				try:
					os.makedirs(os.path.dirname(file_path))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes'])
			index = 1

			for index in range(len(all_atts)):
				all_atts[index].insert(0, user)
				all_atts[index].append('WP')
				filewriter.writerow(all_atts[index])
				index = index + 1 


if __name__ == "__main__":
    main()
















