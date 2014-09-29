from winShare import *
from cvxopt import matrix, solvers
from cvxopt.glpk import ilp
import json
import time
import sys

reignsByYear= {} #{year : [list of reigns]}
reignDict= {} #{reign : index}
indexToReign= {} #{index : reign}

class Reign:
	def __init__(self,p,s,e):
		self.start= s
		self.end= e
		self.wsByYear= [0]*(e-s+1)
		self.player= p

	'''def setYears(s,e):
		self.start= s
		self.end= e
		self.wsByYear= [0]*(e-s+1)'''

	def setWS(ws,year):
		if self.start > year or self.end < year:
			raise Exception("Year not within reign!")
		self.wsByYear[year-self.start]


def getReigns(years):
	prev= years[0][0]
	allReigns= []
	currReign= [(prev, years[0][1])]

	for year,val in years[1:]:
		if year != prev+1:
			allReigns.append(currReign)
			currReign= [(year,val)]
		else: 
			currReign.append((year,val))
		prev= year

	if currReign != []:
		allReigns.append(currReign)

	return allReigns

def firstYear(team):
	currentDir= os.getcwd()
	urls= getURLsOfTeam(team)[::-1] #reverses list
	firstYear= 3000
	for url in urls:
		currYear= int(yearFromURL(url))
		if currYear < firstYear:
			firstYear= currYear
	return firstYear

def getStatLine(team,player,year):
	urls= getURLsOfTeam(team)
	url= ""
	for u in urls:
		if str(year) in u:
			url= u
	currentDir= os.getcwd()
	lists= csvToLists((currentDir + '/teams/' + team + '/' + urlToFilename(url)))

	seasonLine= {}
	seasonLine["name"]=player
	seasonLine["season"]= "\'"+str(year-1)[-2:]+"-\'"+str(year)[-2:]
	seasonLine["year"]= year
	for lst in lists:
		if lst[0]==player:
			seasonLine["teamURL"]= lst[2]
			seasonLine["playerURL"]=lst[1]
			seasonLine["winShares"]= lst[3]
			seasonLine["winSharePct"]= lst[4]
			return seasonLine
	
	seasonLine["teamURL"]= lst[2]
	seasonLine["playerURL"]=lst[1]
	seasonLine["winShares"]= -1
	seasonLine["winSharePct"]= -1
	return seasonLine

def transpose(lst):
	return [list(attr) for attr in zip(*lst)]

def setReignsByYear(team, cutoff):
	global reignsByYear, reignDict, indexToReign
	currentDir= os.getcwd()
	urls= getURLsOfTeam(team)[::-1] #reverses list

	currYear= 0
	eras= {}
	possibles= {}
	playerYears= {}

	#set playerYears dict to contain {playerName : [list of (year,WS) tuples]}
	for url in urls:
		currYear= int(yearFromURL(url))

		if currYear != 2015:
			#bests= {player : [stats]}
			bests= getBestWinSharePlayers(currentDir + '/teams/' + team + '/' + urlToFilename(url),cutoff)
			bests= [(k,v) for (k,v) in bests.iteritems() if k != "all"]
			bests= sorted(bests, key=lambda tup: float(tup[1]), reverse=True)

			#bests is now a list of (player, [stats]) tuples sorted by win shares

			for b in bests:
				playerYears[b[0]]= playerYears.get(b[0],[]) + [(currYear,b[1])]
	
	#here is where I might fill year gaps (i.e. continuous string of years with one gap)

	#split each player's sets of years into contiguous "reigns"
	reigns= []
	playerYears= playerYears.iteritems()
	for (k,v) in playerYears:
		reigns += [(k,r) for r in getReigns(v)] 

	#populate reignsByYear dict to contain {year : [list of reigns containing that year]}
	index= 0
	for (playerName,reign) in reigns:
		yrStart= reign[0][0]
		yrEnd= reign[-1][0]
		r= Reign(playerName,yrStart,yrEnd)
		reignDict[r]= index
		indexToReign[index]= r
		index += 1
		for yr in range(yrStart,yrEnd+1):
			reignsByYear[yr]= reignsByYear.get(yr,[]) + [r]
			r.wsByYear[yrStart-yr]= reign[yrStart-yr][1]

	#print [(k,[r.player for r in v]) for (k,v) in reignsByYear.iteritems()]


def genConstraintMatrix(finalCutoff):
	yearEntries= sorted(reignsByYear.iteritems(), key=lambda tup: tup[0])
	numReigns= len(reignDict.keys())
	#print yearEntries
	constraints= []
	for (yr,reigns) in yearEntries:
		coeffs= [0]*numReigns
		for r in reigns:
			coeffs[reignDict[r]]= (-1)*r.wsByYear[yr-r.start]
		constraints.append(coeffs)
	#print constraints, len(constraints), 2015-1947
	#print matrix(constraints), matrix([0.4]*len(constraints)), matrix([1.0]*numReigns), matrix(constraints).T 
	#print numReigns
	return matrix([1.0]*numReigns),matrix(constraints).T, matrix([-finalCutoff]*len(constraints)), matrix([0.0]*numReigns).T, matrix([0.0]), set(range(numReigns)),set(range(numReigns)) 


def solveIP(team, initialCutoff, finalCutoff):
	global reignsByYear, reignDict, indexToReign
	setReignsByYear(team, initialCutoff)
	c,G,h,A,b,I,B= genConstraintMatrix(finalCutoff)
	#sol=solvers.lp(c,A,b)
	(status,x)= ilp(c,G,h,A,b,I,B)
	#print "Num reigns used", sum(list(x))
	#x has value for each reign: 1 if reign should be included, 0 otherwise
	reigns= sorted([(indexToReign[i].player,indexToReign[i].start,indexToReign[i].end) for i,val in enumerate(x) if val==1],key=lambda tup: tup[1])

	playerStats= []
	for player,start,end in reigns:
		entry= {"player": player, "stats": []}
		for year in range(start,end+1):
			seasonLine= getStatLine(team,player,year)
			entry["stats"].append(seasonLine)
		playerStats.append(entry)

	playerStats= consolidateReigns(playerStats)

	reignsByYear= {}
	reignDict= {}
	indexToReign= {}

	with open(os.getcwd()+'/jsons/'+team+'.json', 'w') as outfile:
		json.dump(playerStats, outfile)

	return playerStats

def consolidateReigns(playerStats):
	playerDict= {}
	for ps in playerStats:
		player= ps["player"]
		playerDict[player]= playerDict.get(player,[]) + ps["stats"]

	consolidated= sorted(playerDict.iteritems(), key=lambda ps: ps[1][0]["year"])
	newJSON= [{"player":p,"stats":s} for p,s in consolidated]
	return newJSON


	
def allDataToJSON():
	currentDir= os.getcwd()
	jsonList= []

	teamNames= "BOS"#getImmediateSubdirectories(currentDir)
	teamNames.remove("d3")
	for team in teamNames:
		info= {"team":team, "eras": [], "confFinal": [], "lossFinal": [], "champion": []}
		print team
		eras= calcEras(team)
		for (p,stats) in eras:
			info["eras"].append({"player":p, "stats":stats})
		cf,lf,c= getSuccessfulYears(team)
		info["confFinal"]= cf
		info["lossFinal"]= lf
		info["champion"]= c
		jsonList.append(info)

	with open(currentDir+'/erasIP.json', 'w') as outfile:
		json.dump(jsonList, outfile)	








if __name__ == "__main__":
	start= time.time()
	#["ATL", "BOS", "BRK", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]:
	solveIP(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]))
	print "Time taken:",time.time()-start
