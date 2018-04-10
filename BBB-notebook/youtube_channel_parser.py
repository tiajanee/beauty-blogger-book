from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

youtube = "https://www.youtube.com/user/lilpumpkinpie05/videos"
page = urlopen(youtube)
soup = BeautifulSoup(page, 'lxml')
#print(soup.prettify())


links = []
 
for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    links.append(link.get('href'))
 
print(links)