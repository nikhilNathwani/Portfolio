import string
import time
import os
import urllib
import urllib2
from bs4 import BeautifulSoup

teamNameToAbbrev= {"Atlanta Hawks":"ATL","Boston Celtics":"BOS","Brooklyn Nets":"BRK","Charlotte Hornets":"CHA","Chicago Bulls":"CHI","Cleveland Cavaliers":"CLE","Dallas Mavericks":"DAL","Denver Nuggets":"DEN","Detroit Pistons":"DET","Golden State Warriors":"GSW","Houston Rockets":"HOU","Indiana Pacers":"IND","Los Angeles Clippers":"LAC","Los Angeles Lakers":"LAL","Memphis Grizzlies":"MEM","Miami Heat":"MIA","Milwaukee Bucks":"MIL","Minnesota Timberwolves":"MIN","New Orleans Pelicans":"NOP","New York Knicks":"NYK","Oklahoma City Thunder":"OKC","Orlando Magic":"ORL","Philadelphia 76ers":"PHI","Phoenix Suns":"PHO","Portland Trail Blazers":"POR","Sacramento Kings":"SAC","San Antonio Spurs":"SAS","Toronto Raptors":"TOR","Utah Jazz":"UTA","Washington Wizards":"WAS"}

#saves team image logos to folder FROM sportslogos.net
def getTeamLogos():
	url= "http://www.sportslogos.net/teams/list_by_league/6/National_Basketball_Association/N/logos/"
	usock= urllib2.urlopen(url)
	data= usock.read()
	usock.close()
	query_soup= BeautifulSoup(data)
	#print query_soup.prettify()
	logoList= query_soup.find('ul', {"class" : "logoWall"})
	images= logoList.find_all('img')
	for image in images:
		src= image["src"]
		fileName= teamNameToAbbrev[image.text.strip()]
		urllib.urlretrieve(src, "../teamLogos/"+fileName+".png")
		print src

#saves team image logos to folder FROM sports-logos-screensavers.com
def getTeamLogosSceensavers():
	url= "http://www.sports-logos-screensavers.com/NationalBasketballAssociation.html"
	usock= urllib2.urlopen(url)
	data= usock.read()
	usock.close()
	query_soup= BeautifulSoup(data)
	#print query_soup.prettify()
	imageList= query_soup.find_all('img')
	for i,image in enumerate(imageList):
		print image["src"]
		src= "http://www.sports-logos-screensavers.com/"+image["src"]
		fileName= i#teamNameToAbbrev[image.text.strip()]
		urllib.urlretrieve(src, "../teamLogos/"+str(fileName)+".png")




if __name__=="__main__":
	getTeamLogos()
	