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
	'jeffreestar', 'Jaclynhill1', 'nikkietutorials', 'oliviajadebeauty', 
	'pixiwoo', 'kandeejohnson', 'zoella280390', 'makeupgeektv', 
	'shaaanxo', 'ChloeMorello', 'Laurenbeautyy', 'Missglamorazzi', 'AllThatGlitters21', 
	'Juicystar07', 'beautybybrittneyx', 'GlamLifeGuru', 'CutiePieMarzia',
	'grav3yardgirl', JAMES_CHARLES, 'HauteBrilliance', 'lisaeldridgedotcom'
]

# 25 youtube handles og bloggers that are disenfranchised in beauty community/darker skinned (based on my perception)
DK_YOUTUBER_NAMES = [
	'itsalissaweekly', 'itsmyRayeRaye','BritPopPrincess', 'AndreasChoice',
	'SmartistaBeauty', NYMA_TANG, 'beautycrush', ALYSSA_FOREVER, JASMINE_BROWN, 'Cydbeats', 
	'Irishcel507', 'lilpumpkinpie05', 'luhhsettyxo', 'BeautyByKelliee', 'yellachyk1', 
	'RavenElyseTV', 'MsAaliyahJay', 'beautybyjj', 'peakmill', 'teasedblackpearlz', 'glamtwinz334',
	'backsyncfan', 'Naptural85'
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
	"white.csv",
	"black.csv",
	"all.csv",
	"WP/",
	"BP/",
]

DIR = '/Users/tiaking/Desktop/beauty_blogger-binder'

def main():

	#create_datasets(DATASETS)

	#saves boths lists of names of to a variable to be looped through each function
	names = WP_YOUTUBER_NAMES
	for name in names:
		url = _url(name)
		top_10 = get_top_10(url)
		full_att_list = get_attributes(url, name)
		create_youtuber_csv(url, name, full_att_list)
		insert_in_hue_dataset(name, full_att_list)
		insert_in_all_dataset(name, full_att_list)

def scrape_top_videos(name):
	'''gets all embedded video links in user's channel, appended in desc popularity'''

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
	'''Create url from name'''

	#concatenates file path catered to user channel to access their video links
	if name[0] is "U":
		url = URL + CHANNEL + name + REF 
	else:
		url = URL + USER + name + REF
	
	return url

def get_subscribers(name):

	if name[0] is "U":
		channel_url = URL + CHANNEL + name
	else:
		channel_url = URL + USER + name

	channel = urlopen(channel_url).read()
	soup = BeautifulSoup(channel,'html.parser')

	dirty_subs = soup.find('span', attrs={"class":"yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"})['title']
	subs = int(re.sub('[^0-9]','', dirty_subs))

	return subs


def get_top_10(name):
	'''get top 10 most popular videos for each name'''
	
	popular_vid_links = scrape_top_videos(name)
	index = 0
	ten_links = []
	
	#for loop to only extract first 10 videos
	for index in range(10):
		ten_links.append(popular_vid_links[index])
		index =  index + 1
	return ten_links

def get_attributes(name, user):
	subscribers = get_subscribers(user)
	videos = get_top_10(name)
	#empty list created to hold list of video attributes(views, likes, dislikes)
	all_atts = []
	for video in videos:
		youtuber_list = []
		youtube_path = URL + video
		youtuber_list.append(youtube_path)
		web_page = urlopen(youtube_path)
		video_soup = BeautifulSoup(web_page, 'html.parser')
		#parses through webpage and cleans data to find view count of video
		try:
			spans = str(soup.find('div', {"class":"watch-view-count"}))
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

		youtuber_list.append(subscribers)

		all_atts.append(youtuber_list)

	return all_atts


def create_youtuber_csv(name, user, all_atts):
	#concatenates top_10_links to an empty CSV for every youtuber
	all_atts = get_attributes(name, user) 

	if user in DK_YOUTUBER_NAMES:
		
		#creating file path
		file_path = DATA_FILE_PATH + DATASETS[4] + '{}.csv'.format(user)
		
		#ensures that function does not create a new csv for every link instead of appending
		if not os.path.exists(os.path.dirname(file_path)):
			try:
				os.makedirs(os.path.dirname(file_path))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		
		#creating the CSV, and writing the headers
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['video_link', 'views', 'likes', 'dislikes', 'subscribers'])
			index = 1
			for index in range(len(all_atts)):
				filewriter.writerow(all_atts[index])
				index = index + 1 
	
	if user in WP_YOUTUBER_NAMES:
		
		#creating correct file path
		file_path = DATA_FILE_PATH + DATASETS[3] + '{}.csv'.format(user)
		
		#ensures that function does not create a new csv for every link instead of appending
		if not os.path.exists(os.path.dirname(file_path)):
			try:
				os.makedirs(os.path.dirname(file_path))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
			
		#creating the CSV, and writing the headers
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(['video_link', 'views', 'likes', 'dislikes', 'subscribers'])
			index = 1

			#append all attributes to CSV
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
				except OSError as exc: 
					if exc.errno != errno.EEXIST:
						raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			if os.path.getsize(file_path) == 0:
				filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes', 'subscribers'])

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
				except OSError as exc: 
					if exc.errno != errno.EEXIST:
						raise
		
		with open(file_path, 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter =",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			if os.path.getsize(file_path) == 0:
				filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes', 'subscribers'])
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
			if os.path.getsize(file_path) == 0:
				filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes', 'subscribers', 'type'])

			index = 1


			for index in range(len(all_atts)):
				all_atts[index].append('black')
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
			if os.path.getsize(file_path) == 0:
				filewriter.writerow(['channel','video_link', 'views', 'likes', 'dislikes', 'subscribers', 'type'])
			
			index = 1



			for index in range(len(all_atts)):
				all_atts[index].append('white')
				filewriter.writerow(all_atts[index])
				index = index + 1 



if __name__ == "__main__":
    main()
















