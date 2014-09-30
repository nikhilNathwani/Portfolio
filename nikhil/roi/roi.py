import numpy
import sys
import time
import csv	
import os
import json
from bs4 import BeautifulSoup

teams= ["ATL","BOS","BRK","CHA","CHI","CLE","DAL","DEN","DET","GSW","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHO","POR","SAC","SAS","TOR","UTA","WAS"]

def csvToLists(fn):
	rows= []
	with open(fn) as f:
		for line in f:
			arr= [elem.strip() for elem in line.split(',')]
			rows.append(arr) 
	return rows 

#returns list of {player,ws,salary} dict for selected team/year
def getPlayerStats(team,year):
	parentDir= os.pardir
	lists= csvToLists('../../teams/'+team+'/'+team+"_"+str(year)+'.csv')
	print [ls[0] for ls in lists if len(ls)!=7]
	dicts= [{"name":ls[0],"link":ls[1],"ws":ls[4],"salary":ls[6]} for ls in lists if len(ls)==7]
	return dicts

#generates json of player stats for all teams in selected year
def genRoiJson(year): 
	currentDir= os.getcwd()
	jsonList= [{"team":t,"players":getPlayerStats(t,year)} for t in teams]
	with open(currentDir+'/roi.json', 'w') as outfile:
		json.dump(jsonList, outfile)

if __name__=="__main__":
	start= time.time()
	print genRoiJson(2014)
	print "Time taken:", time.time()-start