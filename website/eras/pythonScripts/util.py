import numpy
import sys
import time
import urllib2
import csv	
import os
import json
from bs4 import BeautifulSoup

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  web scraping  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def grabSiteData(url):
    usock= urllib2.urlopen(url)
    data= usock.read()
    usock.close()
    return BeautifulSoup(data)



'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  string manip  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def urlToFilename(url):
	elems= url[:-5].split("/")
	team_name= elems[2]
	yr= elems[3]
	return team_name+'_'+yr+".csv"

def yearFromURL(f):
	return int(f[f.rfind('/')+1:f.find('.')])



'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  file system  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def getImmediateSubdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def getTeamYearsFromFolder(team):
	currentDir= os.getcwd()
	files= [name for name in os.listdir(currentDir+'/'+team)]
	team_years= []
	for f in files:
		year= f[f.find('_')+1:f.find('.')]
		team_years += [(f,year)]
	return sorted(team_years, key=lambda tup: tup[1])
            


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  csv read/write  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def csvToLists(fn):
	rows= []
	with open(fn) as f:
		for line in f:
			arr= [elem.strip() for elem in line.split(',')]
			rows.append(arr) 
	return rows 

def listsToCSV(lists,fn):
	csv_file= open(fn,'w+')
	csv_wr = csv.writer(csv_file)
	for row in lists:
		csv_wr.writerow(row)
