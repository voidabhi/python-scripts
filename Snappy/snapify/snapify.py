
import unirest
import webbrowser
import pyperclip
import click
import urllib

@click.group()
def snapify():
    pass
	
@click.command()
@click.argument('url',help='url html page to be snapped',default=pyperclip.getcb().strip())
@click.argument('format',help='extension of snapshot image',default='png')
@click.argument('w',help='width of snapshot image',default='1024')
@click.argument('h',help='height of snapshot image',default='800')
def clip(url,format,w,h):	
	response = unirest.get("https://jmillerdesign-url-screenshot.p.mashape.com/api?url="+urllib.quote(url)+"&format="+format+"&width="+w+"&height="+h+"&delay=5",
	  headers={
		"X-Mashape-Authorization": "7cu8k0bYarwTOOPnOFgJQn9nWwt4tr33"
	  }
	);
	try:
	        # copying it to the clipboard
		pyperclip.setcb(response.body['screenshot'])
	except:
		pass
	finally:
		print response.body['message']
	
@click.command()
@click.argument('url',help='url html page to be snapped',default=pyperclip.getcb().strip())
@click.argument('format',help='extension of snapshot image',default='png')
@click.argument('w',help='width of snapshot image',default='1024')
@click.argument('h',help='height of snapshot image',default='800')
def web(url,format,w,h):
	# create a screenshot
	response = unirest.get("https://jmillerdesign-url-screenshot.p.mashape.com/api?url="+urllib.quote(url)+"&format="+format+"&width="+w+"&height="+h+"&delay=5",
	  headers={
		"X-Mashape-Authorization": "7cu8k0bYarwTOOPnOFgJQn9nWwt4tr33"
	  }
	);
	try:
		webbrowser.open(response.body['screenshot'])
	except:
		pass
	finally:
		print response.body['message']
		

snappy.add_command(clip)
snappy.add_command(web)
