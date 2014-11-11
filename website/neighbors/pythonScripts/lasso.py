from sklearn import linear_model
import sys
from dataProcess import *
from model import *

def lasso(attrs,targets, a):
	clf = linear_model.Lasso(alpha=a)
	clf.fit(attrs, targets)
	#print len(clf.coef_), len(allStatDict), clf.coef_
	'''for i,elem in enumerate(clf.coef_):
		if elem != 0:
			print elem, allStatDict[i]'''
	return clf

def lassoCV(attrs, targets):
	clf = linear_model.LassoCV()
	#print clf
	clf.fit(attrs,targets)
	#print "Best alpha:", clf.alpha_
	return clf

def getBestAttrs(data_type, scale,year):
	if data_type=="all_stats":
		attrDict= allStatDict
	elif data_type=="per_game":
		attrDict= perGameDict
	else:
		attrDict= leagueRankDict

	bestAttrs= []
	bestAttrNames= []

	csvToTrainTest('team_data/'+scale+'/'+data_type,'team_data/winPcts',year)
	m,winList,numSeriesCorrect= baselinePlayoffs(year)
	base=numSeriesCorrect

	csvToTrainTest('team_data/'+scale+'/'+data_type,'team_data/winPcts',year)
	clf= lassoCV(attrs["train"],targets["train"])
	preds= []
	for attr in attrs["test"]: 
		#print urls["test"][j], targets["test"][j], clf.predict(attrs["test"][j])
		preds.append(clf.predict(attr))
	m,winList,numSeriesCorrect= playoffEngine(preds,year)

	for i,elem in enumerate(clf.coef_):
		if elem != 0:
			bestAttrs.append(i)
			bestAttrNames.append(attrDict[i])

	diff= numSeriesCorrect-base

	print "Best alpha:", clf.alpha_, numSeriesCorrect-base
	return bestAttrs

def getBestAlpha(data_type, scale, yearStart):
	alphas=[0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.5]
	data_type= 'league_ranks'
	scale= 'rescale'
	if data_type=="all_stats":
		attrDict= allStatDict
	elif data_type=="per_game":
		attrDict= perGameDict
	else:
		attrDict= leagueRankDict
	nums= []
	diffs= []
	bestsAlphas= {}
	alphaAttrs= {}
	alphaAttrNames= {}
	for a in alphas:
		for yr in range(yearStart,2014):
			csvToTrainTest('team_data/'+scale+'/'+data_type,'team_data/winPcts',yr)
			m,winList,numSeriesCorrect= baselinePlayoffs(yr)
			base=numSeriesCorrect

			csvToTrainTest('team_data/'+scale+'/'+data_type,'team_data/winPcts',yr)
			clf= lasso(attrs["train"],targets["train"],a)
			preds= []
			for attr in attrs["test"]: 
				#print urls["test"][j], targets["test"][j], clf.predict(attrs["test"][j])
				pred.append(clf.predict(attr))
			m,winList,numSeriesCorrect= playoffEngine(pred,yr)
			#print numSeriesCorrect
			nums.append(numSeriesCorrect)
			diffs.append(numSeriesCorrect-base)
		#print nums
		#print diffs, max(diffs)
		bestsAlphas[a]= sum(diffs)
		alphaAttrs[a]= []
		alphaAttrNames[a]= []
		for i,elem in enumerate(clf.coef_):
			if elem != 0:
				alphaAttrs[a].append(i)
				alphaAttrNames[a].append(attrDict[i])
		nums= []
		diffs= []
	#print alphaAttrs
	for a in alphas:
		print a,len(alphaAttrs[a]), bestsAlphas[a]
	bestAlpha= max(bestsAlphas.iterkeys(), key=(lambda key: bestsAlphas[key]))
	print "Best alpha:", bestAlpha
	return alphaAttrs[bestAlpha]


if __name__=="__main__":
	#alphas=[0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.5]
	data_type= 'league_ranks'
	scale= 'rescale'
	csvToTrainTest('team_data/'+scale+'/'+data_type,'team_data/winPcts',int(sys.argv[1]))
	lassoCV(attrs["train"],targets["train"])
	print getBestAttrs(data_type, scale, int(sys.argv[1]))