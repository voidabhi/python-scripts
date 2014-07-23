
from bs4 import BeautifulSoup
import requests

TIMESDEAL_URL = "http://timesdeal.com/delhi-ncr-deals/"

# fetching timesdeal markup
r = requests.get(TIMESDEAL_URL)
soup = BeautifulSoup(r.text)

# fetching all deals data and storing it in file
deals = soup.find_all("li",class_="dealBox")
fp = open("deals.json","wb+");
fp.write("var deals = [\n")
for deal in deals:
	fp.write("\t{\n")
	title = deal.findChildren("a", class_="dealdesc")[0].contents[0]
	shop_name=""
	if("@" in title):
		shop_name = title.split("@")[1]
	fp.write("\t\ttitle: \"%s\",\n"%deal.findChildren("a", class_="dealdesc")[0].contents[0])
	fp.write("\t\tdescription: \"%s\",\n"%deal.findChildren("span",class_="deal-discription-txt")[0].findChildren("a")[0].contents[0])
	fp.write("\t\timage : \"%s\",\n"%deal.findChildren("img")[0].get("src"))
	fp.write("\t\tcategory : \"%s\",\n"%deal.find_all("span",class_="catbox")[0].findChildren("span")[0].contents[0])
	fp.write("\t\tvalidity: \"22/7/2014\",\n")
	fp.write("\t\tshop : {\n")
	fp.write("\t\t\t\tname:\"%s\",\n"%shop_name)
	fp.write("\t\t\t\taddress:\"%s\",\n"%deal.findChildren("address")[0].contents[0].strip())
	fp.write("\t\t\t\timage:\"http://media.timesdeal.com/images/times-deal-logo.png\",\n")
	fp.write("\t\t\t\tphone:\"+919450955992\"\n")
	fp.write("\t\t}\n")
	fp.write("\t},\n")

fp.write("];")
	
	

