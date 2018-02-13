from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import httplib2
import re

youtube = "https://www.youtube.com/user/itsalissaweekly/videos?sort=p&view=0&flow=grid"
page = urlopen(youtube).read()
soup = BeautifulSoup(page,'html.parser')
soup.prettify()


links = []
results = soup.find_all('a',{'class':'yt-uix-sessionlink'})
for link in results:
    links.append(link.get("href"))
    print(links)

