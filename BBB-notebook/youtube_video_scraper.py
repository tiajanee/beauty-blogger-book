from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

youtube = "https://www.youtube.com/watch?v=7b3xjuaAttg"
page = urlopen(youtube)
soup = BeautifulSoup(page, 'lxml')
soup.prettify()




un_views_count = str(soup.find('div', class_="watch-view-count"))
views_count = re.sub('[^0-9]','', un_views_count)
views_count = re.sub(',', '', views_count)

un_dislike_count = str(soup.find('button', title="I dislike this", type="button"))
dislike_count =  re.sub('[^0-9,]',' ', un_dislike_count)
dislike_count = re.sub(',', '', dislike_count).split()
del dislike_count[1]


un_likes_amount = str(soup.find('button', title="I like this", type='button'))
likes_count =  re.sub('[^0-9,]',' ', un_likes_amount)
likes_count = re.sub(',', '', likes_count).split()
del likes_count[1]

print("dislikes:", int(dislike_count[0]))
print("likes:", int(likes_count[0]))
print('views:', views_count)

