

import requests
from constants import URL,Status
import time
import sys
import re

def check_pnr_status(pnr):
	r = requests.get(URL%pnr)
	pnrInfo = r.text[2:-2].split('^')
	if len(pnrInfo)==11:
		if pnrInfo[-1] == "CNF":
			return Status.CONFIRMED
	else:
		print(pnrInfo[-1])
		return Status.WAITING
	return Status.INVALID_PNR
	
# adding progress bar
# timer for 15 minutes for retrying
	
	
if __name__=='__main__':
	"""print('Welcome to PNR Status Service...')
	pnr = ''
	try:
		pnr = sys.argv[1]
	except IndexError:
		pnr = raw_input("Enter your pnr number...")
	status = check_pnr_status(pnr)
	while True:
		if status == Status.CONFIRMED:
			print('Ticket Confirmed')
			break
		elif status == Status.WAITING:
			print('Ticket Not Confirmed...Retrying in 10 minutes')
			time.sleep(10*60)
			status = check_pnr_status(pnr)
			break
		else:
			print('Invalid PNR Number')
			break
	print('Thank you for using the service...see you soon!')"""
	test = '~^8226077749^17412^Mahalaxmi Exp^22-7-2014^SLI^KYN^SL^Chart Not Prepared^~^S6 , 61,GN^CNF^~^S6 , 59,GN^CNF^~^S6 , 58,GN^CNF^~'
	format  = r'(~@[a-zA-Z0-9]{2} , [0-9]{2},[a-zA-Z]{2}@.*@~)'
	test = test.replace('^','@')
	pattern = re.compile(format)
	for m in pattern.finditer(test.rstrip()):
		print m.groups()
		print m.group(1)
	"""if(matchObj):
		if matchObj.group():
			print matchObj.group(1)
	else:
		print("Test:%s"%test)"""