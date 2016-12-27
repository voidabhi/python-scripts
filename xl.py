#!/usr/bin/python

#csv upload to gsheet

import logging
import json
import gspread
import time
import re
from oauth2client.client import SignedJwtAssertionCredentials
from Naked.toolshed.shell import muterun_rb

logging.basicConfig(filename='/var/log/gspread.log',format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)

filename = '<google sheet name>'

#OAuth login
json_key = json.load(open('oauth.json'))
"""
    JSON in the form:
        {
          "private_key_id": "",
          "private_key": "",
          "client_email": "",
          "client_id": "",
          "type": "service_account"
        }
"""
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)
if gc:
  logging.info('OAuth succeeded')
else:
  logging.warn('Oauth failed')

now = time.strftime("%c")

# get data from ruby script
response = muterun_rb('script')
if response:
  logging.info('Data collected')
else:
  logging.warn('Could not collect data')

csv = response.stdout
csv = re.sub('/|"|,[0-9][0-9][0-9]Z|Z', '', csv)
csv_lines = csv.split('\n')

#get columns and rows for cell list
column = len(csv_lines[0].split(","))
row = 1
for line in csv_lines:
  row += 1

#create cell range
columnletter = chr((column - 1) + ord('A'))
cell_range = 'A1:%s%s' % (columnletter, row)

#open the worksheet and create a new sheet
wks = gc.open(filename)
if wks:
  logging.info('%s file opened for writing', filename)
else:
  logging.warn('%s file could not be opened', filename)

sheet = wks.add_worksheet(title=now, rows=(row + 2), cols=(column + 2))
cell_list = sheet.range(cell_range)

#create values list
csv = re.split("\n|,", csv)
for item, cell in zip(csv, cell_list):
  cell.value = item

# Update in batch
if sheet.update_cells(cell_list):
  logging.info('upload to %s sheet in %s file done', now, filename)
else:
  logging.warn('upload to %s sheet in %s file failed', now, filename)
