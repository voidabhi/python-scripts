

import re
import requests
from bs4 import BeautifulSoup
from utils import download_file
import os

SUBJECT = 'seo'
INDEX_ENDPOINT = 'http://www.tutorialspoint.com/%s/index.htm'
DOWNLOAD_ENDPOINT = 'http://www.tutorialspoint.com/%s/pdf/%s.pdf'

def get_all_chapters():
	r = requests.get(INDEX_ENDPOINT%SUBJECT)
	soup = BeautifulSoup(r.text)
	links = soup.find_all("a",{"target":"_top"})
	os.makedirs(SUBJECT)
	for link in links:
		if(re.match(r'^/'+SUBJECT,link['href'])):
			filename  = link['href'].split('/')[-1]
			download_file(DOWNLOAD_ENDPOINT%(SUBJECT,filename.split('.')[0]),SUBJECT+'/'+filename.split('.')[0])

get_all_chapters()
