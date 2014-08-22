from winShare import *

reignsByYear= {} #{year : [list of reigns]}
reignDict= {} #{reign : index}

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


def setReignsByYear(team):
	global reignsByYear, reignDict
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
			bests= getBestWinSharePlayers(currentDir + '/' + team + '/' + urlToFilename(url),0.75)
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
		index += 1
		for yr in range(yrStart,yrEnd+1):
			reignsByYear[yr]= reignsByYear.get(yr,[]) + [r]
			r.wsByYear[yrStart-yr]= reign[yrStart-yr][1]

	#print [(k,[r.player for r in v]) for (k,v) in reignsByYear.iteritems()]


def genConstraintMatrix():
	yearEntries= sorted(reignsByYear.iteritems(), key=lambda tup: tup[0])
	numReigns= len(reignDict.keys())
	#print yearEntries
	constraints= []
	for (yr,reigns) in yearEntries:
		coeffs= [0]*numReigns
		for r in reigns:
			coeffs[reignDict[r]]= r.wsByYear[yr-r.start]
		constraints.append(coeffs)
	print constraints, len(constraints), 2015-1947
	return constraints

	
	








if __name__ == "__main__":
	setReignsByYear("BOS")
	genConstraintMatrix()
	#print firstYear("BOS")
	#print getReigns([0,1,2,3,5,6,9,10,11,12,18,23,24])