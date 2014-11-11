import string
import time
import csv
import sys
import numpy as np
from model import *

allStatDict= {0:'FG',1:'FGA',2:'FG%',3:'3P',4:'3PA',5:'3P%',6:'2P',7:'2PA',8:'2P%',9:'FT',10:'FTA',11:'FT%',12:'ORB',13:'DRB',14:'TRB',15:'AST',16:'STL',17:'BLK',18:'TOV',19:'PF',20:'PTS',21:'FG_rank',22:'FGA_rank',23:'FG%_rank',24:'3P_rank',25:'3PA_rank',26:'3P%_rank',27:'2P_rank',28:'2PA_rank',29:'2P%_rank',30:'FT_rank',31:'FTA_rank',32:'FT%_rank',33:'ORB_rank',34:'DRB_rank',35:'TRB_rank',36:'AST_rank',37:'STL_rank',38:'BLK_rank',39:'TOV_rank',40:'PF_rank',41:'PTS_rank',42:'FG_opp',43:'FGA_opp',44:'FG%_opp',45:'3P_opp',46:'3PA_opp',47:'3P%_opp',48:'2P_opp',49:'2PA_opp',50:'2P%_opp',51:'FT_opp',52:'FTA_opp',53:'FT%_opp',54:'ORB_opp',55:'DRB_opp',56:'TRB_opp',57:'AST_opp',58:'STL_opp',59:'BLK_opp',60:'TOV_opp',61:'PF_opp',62:'PTS_opp',63:'FG_opp_rank',64:'FGA_opp_rank',65:'FG%_opp_rank',66:'3P_opp_rank',67:'3PA_opp_rank',68:'3P%_opp_rank',69:'2P_opp_rank',70:'2PA_opp_rank',71:'2P%_opp_rank',72:'FT_opp_rank',73:'FTA_opp_rank',74:'FT%_opp_rank',75:'ORB_opp_rank',76:'DRB_opp_rank',77:'TRB_opp_rank',78:'AST_opp_rank',79:'STL_opp_rank',80:'BLK_opp_rank',81:'TOV_opp_rank',82:'PF_opp_rank',83:'PTS_opp_rank',84:'MOV',85:'SOS',86:'SRS',87:'ORtg',88:'DRtg',89:'Pace',90:'FTr',91:'3PAr',92:'eFG%_off',93:'TOV%_off',94:'ORB%_off',95:'FT/FGA_off',96:'eFG%_def',97:'TOV%_def',98:'DRB%_def',99:'FT/FGA_def',100:'MOV_rank',101:'SOS_rank',102:'SRS_rank',103:'ORtg_rank',104:'DRtg_rank',105:'Pace_rank',106:'FTr_rank',107:'3PAr_rank',108:'eFG%_off_rank',109:'TOV%_off_rank',110:'ORB%_off_rank',111:'FT/FGA_off_rank',112:'eFG%_def_rank',113:'TOV%_def_rank',114:'DRB%_def_rank',115:'FT/FGA_def_rank'}
perGameDict= {0: 'FG', 1: 'FGA', 2: 'FG%', 3: '3P', 4: '3PA', 5: '3P%', 6: '2P', 7: '2PA', 8: '2P%', 9: 'FT', 10: 'FTA', 11: 'FT%', 12: 'ORB', 13: 'DRB', 14: 'TRB', 15: 'AST', 16: 'STL', 17: 'BLK', 18: 'TOV', 19: 'PF', 20: 'PTS', 21: 'FG_opp', 22: 'FGA_opp', 23: 'FG%_opp', 24: '3P_opp', 25: '3PA_opp', 26: '3P%_opp', 27: '2P_opp', 28: '2PA_opp', 29: '2P%_opp', 30: 'FT_opp', 31: 'FTA_opp', 32: 'FT%_opp', 33: 'ORB_opp', 34: 'DRB_opp', 35: 'TRB_opp', 36: 'AST_opp', 37: 'STL_opp', 38: 'BLK_opp', 39: 'TOV_opp', 40: 'PF_opp', 41: 'PTS_opp', 42: 'MOV', 43: 'SOS', 44: 'SRS', 45: 'ORtg', 46: 'DRtg', 47: 'Pace', 48: 'FTr', 49: '3PAr', 50: 'eFG%_off', 51: 'TOV%_off', 52: 'ORB%_off', 53: 'FT/FGA_off', 54: 'eFG%_def', 55: 'TOV%_def', 56: 'DRB%_def', 57: 'FT/FGA_def'}
leagueRankDict= {0: 'FG_rank', 1: 'FGA_rank', 2: 'FG%_rank', 3: '3P_rank', 4: '3PA_rank', 5: '3P%_rank', 6: '2P_rank', 7: '2PA_rank', 8: '2P%_rank', 9: 'FT_rank', 10: 'FTA_rank', 11: 'FT%_rank', 12: 'ORB_rank', 13: 'DRB_rank', 14: 'TRB_rank', 15: 'AST_rank', 16: 'STL_rank', 17: 'BLK_rank', 18: 'TOV_rank', 19: 'PF_rank', 20: 'PTS_rank', 21: 'FG_opp_rank', 22: 'FGA_opp_rank', 23: 'FG%_opp_rank', 24: '3P_opp_rank', 25: '3PA_opp_rank', 26: '3P%_opp_rank', 27: '2P_opp_rank', 28: '2PA_opp_rank', 29: '2P%_opp_rank', 30: 'FT_opp_rank', 31: 'FTA_opp_rank', 32: 'FT%_opp_rank', 33: 'ORB_opp_rank', 34: 'DRB_opp_rank', 35: 'TRB_opp_rank', 36: 'AST_opp_rank', 37: 'STL_opp_rank', 38: 'BLK_opp_rank', 39: 'TOV_opp_rank', 40: 'PF_opp_rank', 41: 'PTS_opp_rank', 42: 'MOV_rank', 43: 'SOS_rank', 44: 'SRS_rank', 45: 'ORtg_rank', 46: 'DRtg_rank', 47: 'Pace_rank', 48: 'FTr_rank', 49: '3PAr_rank', 50: 'eFG%_off_rank', 51: 'TOV%_off_rank', 52: 'ORB%_off_rank', 53: 'FT/FGA_off_rank', 54: 'eFG%_def_rank', 55: 'TOV%_def_rank', 56: 'DRB%_def_rank', 57: 'FT/FGA_def_rank'}
leagueRankDictAbbrev={ 0: 'FG', 1: 'FGA', 2: 'FG%', 3: '3P', 4: '3PA', 5: '3P%', 6: '2P', 7: '2PA', 8: '2P%', 9: 'FT', 10: 'FTA', 11: 'FT%', 12: 'ORB', 13: 'DRB', 14: 'TRB', 15: 'AST', 16: 'STL', 17: 'BLK', 18: 'TOV', 19: 'PF', 20: 'PTS', 21: 'FG_opp', 22: 'FGA_opp', 23: 'FG%_opp', 24: '3P_opp', 25: '3PA_opp', 26: '3P%_opp', 27: '2P_opp', 28: '2PA_opp', 29: '2P%_opp', 30: 'FT_opp', 31: 'FTA_opp', 32: 'FT%_opp', 33: 'ORB_opp', 34: 'DRB_opp', 35: 'TRB_opp', 36: 'AST_opp', 37: 'STL_opp', 38: 'BLK_opp', 39: 'TOV_opp', 40: 'PF_opp', 41: 'PTS_opp', 42: 'MOV', 43: 'SOS', 44: 'SRS', 45: 'ORtg', 46: 'DRtg', 47: 'Pace', 48: 'FTr', 49: '3PAr', 50: 'eFG%_off', 51: 'TOV%_off', 52: 'ORB%_off', 53: 'FT/FGA_off', 54: 'eFG%_def', 55: 'TOV%_def', 56: 'DRB%_def', 57: 'FT/FGA_def'}
statDicts= {"all_stats":allStatDict, "per_game":perGameDict, "league_ranks":leagueRankDictAbbrev}


#returns dict with "train" and "test" lists of Team data
#test list has teams from year "year_rank", train has teams from years < "year"
def csvToTrainTest(csv, winPctFN, year):
    global attrs,urls,targets,indexDict,teamsByYear,winPcts
    datafile = open(csv, 'r')
    winPctFile= open(winPctFN,'r')
    count= {"train":0,"test":0,"other":0}
    for i,row in enumerate(datafile):
        stats= [elem for elem in row.strip().split(',')]
        attr= [float(elem) for elem in stats[:-2]]
        yr= yearFromURL(stats[-2])
        if year==yr:
            key= "test"
        elif yr<year:
            key= "train"
        else:
            key= "other"
        if count[key]==0:
            attrs[key]= []
            urls[key]= []
            targets[key]= []
        attrs[key].append(attr) #append feature vector to attrs
        urls[key].append(stats[-2])
        targets[key].append(float(stats[-1]))
        if key=="test": 
            indexDict[stats[-2]]= count["test"]
        count[key] += 1

    count= {"train":0,"test":0,"other":0}
    #store contents of winPcts file    
    for i,row in enumerate(winPctFile):
        stats= [elem for elem in row.strip().split(',')]
        yr= yearFromURL(stats[-1])
        if year==yr:
            key= "test"
        elif yr<year:
            key= "train"
        else:
            key= "other"
        if count[key]==0:
            winPcts[key]= []
        winPcts[key].append(float(stats[0]))
        count[key] += 1

def getWinPct(team_url):
    soup= grabSiteData("http://www.basketball-reference.com"+team_url)
    recordPar= [p for p in soup.findAll('p') if "Record:" in p.text]
    recordString= recordPar[0].text.encode("utf8","ignore")
    record= recordString[recordString.find(" ")+1:recordString.find(",")]
    wins,losses= [float(s) for s in record.split("-")]
    return wins/(wins+losses)

#input name of one of the training data files to get URLs in correct order
def storeWinPcts(fn):
    winPctRows= []
    datafile = open(fn, 'r')
    for i,row in enumerate(datafile):
        print "Row:", i
        stats= [elem for elem in row.strip().split(',')]
        url= stats[-2]
        winPctRows.append([getWinPct(url),url])
    listsToCSV(winPctRows,'team_data/winPcts')
 
#fetches beautifulsoup-formatted data from given url
def grabSiteData(url):
    usock= urllib2.urlopen(url)
    data= usock.read()
    usock.close()
    return BeautifulSoup(data)

def csvToLists(fn):
	rows= []
	with open(fn) as f:
		for line in f:
			arr= [line.split(',')]
			rows += arr 
	return rows 

def listsToCSV(lists,fn):
	csv_file= open(fn,'wb')
	csv_wr = csv.writer(csv_file)
	for row in lists:
		csv_wr.writerow(row)

def transpose(lst):
	return [list(attr) for attr in zip(*lst)]

#un-ignore wins_pyth and losses_pyth if lockout season stats are scaled properly
statsToIgnore= ["player","g", "mp", "arena_name", "attendance", "wins_pyth", "losses_pyth"]

#returns dictionary of (playoff_team_url,num_wins_in_playoffs) pairs
def getPlayoffTeams(year):
    teams_wins= {} #counts number of series each team won in a given playoff year
    query_soup= grabSiteData("http://www.basketball-reference.com/playoffs/NBA_"+str(year)+".html")
    playoff_data= query_soup.find('div', {"id" : "all_playoffs"}).findAll('tr', {"class" : "mobile_text"})
    for row in playoff_data:
        tds= row.findAll("td")
        p_round= tds[0].text.encode("ascii","ignore")
        #if "First" not in p_round:
        record_index= p_round.find('(')
        wins= [int(p_round[record_index+1]), int(p_round[record_index+3])]
        matchup= [elem["href"].encode("ascii","ignore") for elem in tds[1].findAll("a")][:-1]
        for i,team in enumerate(matchup):
            #add 1 to "team" if that team won the series, 0 otherwise
            teams_wins[team]= teams_wins.get(team,0) + (wins[i] > wins[not i])
    return teams_wins


#id is id of table div in query soup
def scrapeTeamStatsFromTable(id, query_soup, all_stats, per_game, lg_ranks):
    #get list of indices containing stats I care about
    div= query_soup.find('div', {"class" : "table_container", "id" : id})
    header= div.find("thead").findAll('tr')[-1]
    indices= []
    for i,elem in enumerate(header.findAll('th')): 
        if elem['data-stat'] not in statsToIgnore:
            indices += [i]

    #get stats located in desired indices
    stat_rows= div.findAll("tr")
    for row in stat_rows:
        statline= row.findAll('td')
        arraysToAddTo= []
        if len(statline) != 0: #statline is [] for table header rows
            #kind of janky
            if statline[0].text.encode("ascii","ignore")=="Lg Rank":
                arraysToAddTo += [lg_ranks,all_stats]
            if statline[0].text.encode("ascii","ignore") in ["Team/G", "Opponent/G"]: 
                arraysToAddTo += [per_game,all_stats]
            if statline[0].text.encode("ascii","ignore")=="Team" and id=="div_team_misc":
                arraysToAddTo += [per_game,all_stats]
            for j in indices:
                for arr in arraysToAddTo:
                    value= float(statline[j].text.encode("ascii","ignore").replace("%",""))
                    arr += [value]
    return (all_stats, per_game, lg_ranks)
    

#returns (all_stats, per_game, lg_ranks) tuple of arrays
def scrapeTeamStats(team_url):
    all_stats= []
    per_game= []
    lg_ranks= []
    soup= grabSiteData("http://www.basketball-reference.com"+team_url)

    #ids of tables I want to scrape from
    arr= (all_stats, per_game, lg_ranks)
    table_ids= ["div_team_stats", "div_team_misc"]
    for id in table_ids:
        (all_stats, per_game, lg_ranks)= scrapeTeamStatsFromTable(id, soup, all_stats, per_game, lg_ranks)
    
    return (all_stats, per_game, lg_ranks) 


#statType= 0 for all_stats, 1 for per_game, 2 for lg_ranks
def createTrainingSets(yearStart, yearEnd, folder, fn_all_stats, fn_per_game, fn_lg_ranks):
    #create CSVs and csv_writers
    asCSV= open(folder+fn_all_stats,'wb') #"as" for "all stats"
    pgCSV= open(folder+fn_per_game,'wb')  #"pg" for "per game"
    lrCSV= open(folder+fn_lg_ranks,'wb')  #"lr" for "league ranks"
    as_wr = csv.writer(asCSV)
    pg_wr = csv.writer(pgCSV)
    lr_wr = csv.writer(lrCSV)

    #populate CSVs
    for year in range(yearStart, yearEnd+1): 
        playoff_teams= getPlayoffTeams(year)
        for url,wins in playoff_teams.items():
            arrs= (all_stats,per_game,lg_ranks)= scrapeTeamStats(url)
            for arr in arrs:
                arr += [url, wins]
            as_wr.writerow(all_stats)
            pg_wr.writerow(per_game)
            lr_wr.writerow(lg_ranks)
        print "Done with year", year


def getPlayoffStandings(year):
    query_soup= grabSiteData("http://www.basketball-reference.com/leagues/NBA_"+str(year)+".html")
    confs= {"east":[0]*8,"west":[0]*8}
    for conf in confs:
        standings_div= query_soup.find('div', {"id" : "div_"+conf[0].upper()+"_standings"})
        teams= standings_div.findAll('td', {"align" : "left"})
        for team in teams:
            url= str(team.find('a')['href'])
            rank= int(team.find('span').text[1:-1])
            if rank<9:
                confs[conf][rank-1]= [url]
        csv_file= open("standings/"+conf+"/"+str(year),'wb')
        wr= csv.writer(csv_file)
        for url in confs[conf]:
            print url
            wr.writerow(url)

#standardizes each attribute by "RESCALING": subtracting min and dividing by (max-min)
#-old_data_fn is the name of the CSV to be normalized
#-new_data_fn is the name of the CSV into which ,the normalized data should be placed. 
#   If equal to old_data_fn, then old_data_fn is overwritten
#-file_base is all_stats, per_game, or league_ranks
def standardizeRescale(scale,name):
	old_data_fn= 'team_data/raw/'+name
	new_data_fn= 'team_data/'+scale+'/'+name
	scale_fn= 'scales/'+scale+'/'+name+'_scales'
	mins, diffs= [[],[]]

	#get team data from file	
	rows= csvToLists(old_data_fn)
	cols= transpose(rows)
	for i in range(len(cols)-2): #The url and the label columns are skipped over.
		#prepare to save min and diff data to file
		data=[float(x) for x in cols[i]]
		mins += [float(min(data))]
		diffs += [float(max(data))-mins[i]]
		cols[i]= [(float(elem)-mins[i])/diffs[i] for elem in cols[i]]
	cols[-1]= [float(x) for x in cols[-1]] #convert label column entries to floats
	
	#save normalized data to new file
	listsToCSV(transpose(cols),new_data_fn)
	
	#save scaling info (mins and diffs) to file 
	listsToCSV([mins,diffs],scale_fn)


def standardizeNorm(scale,name):
	old_data_fn= 'team_data/raw/'+name
	new_data_fn= 'team_data/'+scale+'/'+name
	scale_fn= 'scales/'+scale+'/'+name+'_scales'
	norms=[]

	#get train/test data from file	
	rows= csvToLists(old_data_fn)
	cols= transpose(rows)
	for i in range(len(cols)-2):
		#prepare to save min and diff data to file
		data= [float(elem) for elem in cols[i]]
		norms += [np.linalg.norm(data)]
		cols[i]= [float(elem)/norms[i] for elem in cols[i]]
	cols[-1]= [float(x) for x in cols[-1]] #convert label column entries to floats
	
	#save normalized data to new file
	listsToCSV(transpose(cols),new_data_fn)
	
	#save scaling info (mins and diffs) to file 
	listsToCSV([norms],'scales/norm/'+file_base+'_scales')