import webbrowser, sys

#fetching the query from command lines
if len(sys.argv) > 1:
    #get from command line
    address = ' '.join(sys.argv[1:]).strip()
else:
    # get from clipboard
    import pyperclip
    address = pyperclip.getcb().strip()

#appending to map url address
googlemapsurl = 'http://maps.google.com/maps?q='
if sys.version.startswith('2.'): # for Python 2 version
    import urllib
    googlemapsurl += urllib.quote(address)
else:
    import urllib.parse
    googlemapsurl += urllib.parse.quote(address)

#showing map url in browser
webbrowser.open(googlemapsurl)
