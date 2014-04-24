

import requests,sys
import pyperclip

def download_file(url,filename):
	print 'Downloading file %s'%filename
	
	with open(filename,"wb") as f:
		r = requests.get(url,stream=True)
		length = r.headers.get('content-length')
		if length is None:
			f.write(r.content)
		else:
			dl=0
			for chunk in r.iter_content():
				f.write(chunk)
				# sys.stdout.write("\r[%d]"%(done,))
				sys.stdout.flush()

if(__name__=='__main__'):
	url = pyperclip.getcb().strip()
	download_file(url,url.split('/')[-1])