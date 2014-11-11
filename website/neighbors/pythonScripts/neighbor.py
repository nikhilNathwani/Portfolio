import sys
import math
import numpy as np
import time
import matplotlib.pyplot as plot
import json
from random import shuffle
from model import *
from dataProcess import *
from sklearn import neighbors
from lasso import *

#weight is "uniform" or "distance", where distance weights 
#votes according to inverse euclidean distance
#data_type is all_stats, per_game, or league_ranks
def kNNEngine(k,reg,data_type,weight="distance"):
    #create classifier
    clf= neighbors.KNeighborsRegressor(k,weight) if reg else neighbors.KNeighborsClassifier(k,weight)
    #print "knnEngine",attrs["train"], targets["train"]
    clf.fit(attrs["train"], targets["train"])

    predictions= []
    #run kNN for each test point
    for index,attr in enumerate(attrs["test"]):
        #print "\n\n\n\nPredicting", urls["test"][index]
        x= clf.kneighbors(list(attr)) #returns array([distances list],[neighbor index list])
        [dists, neighs]= [x[0][0], x[1][0]]
        #print results
        '''print "         Neighbor        Wins   Similarity"
        for i in range(len(neighs)):
            if i<=8:
                print str(i+1)+". ", urls["train"][neighs[i]], targets["train"][neighs[i]], dists[i], xMostSimilarAttributes(5,index,neighs[i],data_type)
            else:
                print str(i+1)+".", urls["train"][neighs[i]], targets["train"][neighs[i]], dists[i], xMostSimilarAttributes(5,index,neighs[i],data_type)'''
        predictions.append(float(clf.predict(attr))) #save prediction to predictions dict
    return predictions

def neighborsToJSON(k,num_attrs,weight="distance"):
    #create classifier
    clf= neighbors.KNeighborsRegressor(k,weight)
    clf.fit(attrs["train"], targets["train"])

    #construct dict of json neighbor lists for each team
    order= {teamName(k):v for k, v in indexDict.items()} #{"IND":0,"MIA":1,"TOR":2,"CHI":3,"WAS":4,"BRK":5,"CHA":6,"ATL":7,"SAS":8,"OKC":9,"LAC":10,"HOU":11,"POR":12,"GSW":13,"MEM":14,"DAL":15}
    testList= [0]*16
    predictions= []

    for testInd in range(16):
        #get neighbors of test point at index testInd
        testAttr= attrs["test"][testInd]
        x= clf.kneighbors(list(testAttr))
        [dists, neighs]= [x[0][0], x[1][0]]
        predictions.append(float(clf.predict(testAttr))) 

        permuter= range(len(neighs))
        shuffle(permuter)
        neighs= [neighs[p] for p in permuter]
        dists= [dists[p] for p in permuter]

        neighList= []
        for i,n in enumerate(neighs):
            #populate neighbor data and add to neighList
            d= dists[i]
            url= urls["train"][n]
            data= {}
            data["name"]=teamName(url)
            year= yearFromURL(url)
            data["year"]= '\''+str(year-1)[-2:]+'-\''+str(year)[-2:]
            data["url"]= url
            data["wins"]= targets["train"][n]
            data["dist"]= d
            data["attrs"]= [elem[0] for elem in xMostSimilarAttributes(num_attrs,testInd,n)]
            neighList.append(data)
        #add neighList to testList
        tn=teamName(urls["test"][testInd])
        testList[order[tn]]= {"team":tn, "neighbors":neighList}
    matchups,wins,num_series_correct= kNNPlayoffs(predictions,2014)
    for i,entry in enumerate(testList):
        entry["predictedWins"]= wins[i]

    newOrder= {"IND":0,"MIA":1,"TOR":2,"CHI":3,"WAS":4,"BRK":5,"CHA":6,"ATL":7,"SAS":8,"OKC":9,"LAC":10,"HOU":11,"POR":12,"GSW":13,"MEM":14,"DAL":15}
    testListReordered= [0]*16
    for tl in testList:
        testListReordered[newOrder[tl["team"]]]= tl

    print json.dumps(testListReordered, sort_keys=True, indent=4, separators=(',', ': '))
    #with open('../../../finalSite/nikhil/neighbors/neighbors.json', 'w') as outfile:
    #    json.dump(testListReordered, outfile)
    print predictions
    print sorted([(k,predictions[v]) for k,v in indexDict.iteritems()], key=lambda p: p[1])


def kNN(k,data_type,weight="distance"):
    return kNNEngine(k,False,data_type,weight)

def regressionKNN(k,data_type,weight="distance"):
    return kNNEngine(k,True,data_type,weight)

#test is the test team and train is the train team
def xMostSimilarAttributes(x,test, train, data_type="league_ranks"):
    te= attrs["test"][test]
    tr= attrs["train"][train]
    diffs= [(abs(te[i]-tr[i]),i) for i in range(len(te))]
    diffs.sort()
    return [(statDicts[data_type][ind],diff) for (diff,ind) in diffs[:x]]


def euclideanError(teams):
    trues= np.array([t.true_label for t in teams])
    predicts= np.array([t.predicted_label for t in teams])
    return np.linalg.norm(trues-predicts)

def reportPlayoffAccuracy(year):
    x= range(1,30) 
    results= []
    for k in x:
        for scale in scales:
            for dt in data_types:
                data= csvToTrainTest("team_data/"+scale+"/"+dt, year)
                [train,test]= [data["train"], data["test"]]
                for team in test:
                    weightedKNN(j, train, team)
                pt= PlayoffTree(year, test,False)
                results[dt] +=[euclideanError(test)]
                print "Scale:", scale, "Type:", dt, "Error:",str(euclideanError(test))
    plot.plot(x,results["league_ranks"],'r-', label="League Ranks")
    plot.plot(x,results["all_stats"],'b-', label="All Stats")
    plot.plot(x,results["per_game"],'g-', label="Per Game")
    #plot.axis( [0, 50, 0, 14])
    plot.xlabel( "k Value" )
    plot.ylabel( "Euclidean Error" )
    plot.show()

def compareErrors(year):
    scale= 'rescale'
    pred= []
    d="all_stats"
    diffs= []
    bestAttrsByYear= {}
    for k in range(1,50):
        for yr in range(year,2015): 
            #remove attrs that aren't the best
            if yr in bestAttrsByYear:
                bestAttrs= bestAttrsByYear[yr]
            else:
                bestAttrs= getBestAttrs(d, scale, yr)
                bestAttrsByYear[yr]= bestAttrs
            thinDicts(bestAttrs)

            csvToTrainTest('team_data/'+scale+'/'+d,'team_data/winPcts',yr)
            m,winList,numSeriesCorrect= baselinePlayoffs(yr)
            base=numSeriesCorrect
            #print "Year:", yr, "Base:", base

            csvToTrainTest('team_data/'+scale+'/'+d,'team_data/winPcts',yr)
            p=regressionKNN(k,d,"distance")
            m,winList,numSeriesCorrect= kNNPlayoffs(p,yr)
            pred.append(numSeriesCorrect)
            diffs.append(numSeriesCorrect-base)

            #print "Year:",yr, "Baseline:", base, "Predicted:", numSeriesCorrect

        print k,diffs,pred, sum(diffs), float(sum(diffs))/len(diffs)
        pred= []
        diffs= []
  
        '''
        plot.plot(range(year,2015),pred,'r-', label="Pred")
        plot.plot(range(year,2015),base,'b-', label="Base")
        #plot.axis( [0, 50, 0, 14])
        plot.xlabel( "k Value" )
        plot.ylabel( "Num Series Correct" )
        plot.show() '''

if __name__=='__main__':
    start= time.time()
    scale= "rescale"
    d= "league_ranks"
    yr= 2014
    csvToTrainTest('team_data/'+scale+'/'+d,'team_data/winPcts',yr)
    neighborsToJSON(int(sys.argv[1]),int(sys.argv[2]))
    print "Time taken:", time.time()-start