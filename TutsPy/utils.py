

import requests,sys
import random

def download_file(url,filename):
	print 'Downloading file %s'%filename
	
	with open("%s.pdf"%filename,"wb") as f:
		r = requests.get(url,stream=True)
		length = r.headers.get('content-length')
		if length is None:
			f.write(r.content)
		else:
			dl=0
			for chunk in r.iter_content():
				dl+=len(chunk)
				done =int(dl/int(length))
				f.write(chunk)
				sys.stdout.write("\r[%d%%]"%(done*100))
				sys.stdout.flush()

if(__name__=='main'):
	download_file('http://www.lucas.lth.se/events/2002/Clements020306.PDF',str(random.random()))