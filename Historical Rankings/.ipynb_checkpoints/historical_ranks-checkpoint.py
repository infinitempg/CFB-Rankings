import json
import pandas as pd
import numpy as np
from tqdm.autonotebook import tqdm
from sklearn import preprocessing
import urllib
import os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

curWeek = 17

P5 = ['ACC','Pac-12','Big Ten','Big 12','SEC','Notre Dame']
G5 = ['Conference USA','Sun Belt','Mid-American','American Athletic','Mountain West','FBS Independents']

def seasonProgression(dfR):
    totalGames = len(dfR)
    cWeek = int(dfR['week']) + 1
    return cWeek/(2*totalGames)

def winningTeam(dfR):
    if dfR['home_points'] > dfR['away_points']:
        return dfR['home_team']
    else:
        return dfR['away_team']
    
def teamWin(dfR, team):
    if dfR.winner == team:
        return True
    else:
        return False
    
def findOpp(dfR):
    if dfR.home == True:
        return dfR.away_team
    else:
        return dfR.home_team
def findOppConf(dfR):
    if dfR.home == True:
        return dfR.away_conference
    else:
        return dfR.home_conference
    
def locMult(dfR):
    if dfR['neutral_site'] == True:
        return 1.05
    elif dfR['home'] == True:
        return 1.1
    else:
        return 1.
    
def pointDiff(dfR,team):
    if dfR.home_team == team:
        return dfR.home_points - dfR.away_points
    else:
        return dfR.away_points - dfR.home_points
    
def confMult(dfR):
    if dfR.opp_conference in P5:
        return 1.
    elif dfR.opp_conference in G5:
        return 0.5
    else:
        return 0.15
    
def winQ(dfR,week,FBSdict): 
    if dfR.opp_conference == None:
        oppWinPct = 0.5
    else:
#         print(dfR.opp_conference)
        oppWinPct = FBSdict[dfR.opp].loc[FBSdict[dfR.opp].week <= week, 'winPct'].tail(1).item()
    
    if dfR.teamWin == True:
        winMult = 1
        oppFactor = oppWinPct
    else:
        winMult = -1
        oppFactor = 1 - oppWinPct
    
    return oppFactor * dfR.seasonProg * dfR.conf_mult * winMult*(dfR.loc_mult + 0.01*dfR.point_diff)

def calcPct(team, week,FBSdict):
    winqweek = 'win_q_'+str(week)
    wins = FBSdict[team].loc[FBSdict[team].week <= week, 'wins'].tail(1).item()
    losses = FBSdict[team].loc[FBSdict[team].week <= week, 'losses'].tail(1).item()
    return 0.9 * FBSdict[team][winqweek].mean() + 0.01*(wins-losses)

def getRanks(year):
    json_url = urllib.request.urlopen('https://api.collegefootballdata.com/games?year=%s&seasonType=regular'%year)
    jsonFile = json.loads(json_url.read())
    curSch = pd.DataFrame(jsonFile)
    
    json_url2 = urllib.request.urlopen('https://api.collegefootballdata.com/games?year=%s&seasonType=postseason'%year)
    jsonFile2 = json.loads(json_url2.read())
    postSch = pd.DataFrame(jsonFile2)
    postSch['week'] = postSch['week'] + 15
    curSch = curSch.append(postSch)

    curSch.loc[curSch.away_team == 'Notre Dame','away_conference'] = 'Notre Dame'
    curSch.loc[curSch.home_team == 'Notre Dame','home_conference'] = 'Notre Dame'

    FBSteams = curSch['home_team'].unique()
    FBSteams.sort()

    FBSdict = {}
    for team in FBSteams:
        FBSdict[team] = curSch[(curSch['away_team'] == team) | 
                               (curSch['home_team'] == team)]
        FBSdict[team] = FBSdict[team][np.isfinite(FBSdict[team].away_points)]
        FBSdict[team] = FBSdict[team].reset_index()

    print('Calculating variables:')
    FBSbar = tqdm(total=len(FBSteams))
    for key in FBSdict:
        FBSbar.set_description(key)
        FBSdict[key]['seasonProg'] = FBSdict[key].apply(lambda row: seasonProgression(row),axis = 1)
        FBSdict[key]['winner'] = FBSdict[key].apply(lambda row: winningTeam(row),axis = 1)
        FBSdict[key]['teamWin'] = FBSdict[key].apply(lambda row: teamWin(row,key),axis = 1)

        wins = 0
        losses = 0
        winList = []
        lossList = []
        for row in FBSdict[key].itertuples():
        #     print(row.winner)
            if row.teamWin:
                wins += 1
            else:
                losses += 1
            winList.append(wins)
            lossList.append(losses)

        FBSdict[key]['wins'] = winList
        FBSdict[key]['losses'] = lossList

        hometeam = FBSdict[key]['home_team'] == key
        FBSdict[key]['home'] = hometeam

        FBSdict[key]['winPct'] = FBSdict[key]['wins']/(FBSdict[key]['losses'] + FBSdict[key]['wins'])
        FBSdict[key]['opp'] = FBSdict[key].apply(lambda row: findOpp(row), axis = 1)
        FBSdict[key]['opp_conference'] = FBSdict[key].apply(lambda row: findOppConf(row), axis = 1)
        FBSdict[key]['point_diff'] = FBSdict[key].apply(lambda row: pointDiff(row,key), axis = 1)
        FBSdict[key]['loc_mult'] = FBSdict[key].apply(lambda row: locMult(row), axis = 1)
        FBSdict[key]['conf_mult'] = FBSdict[key].apply(lambda row: confMult(row), axis = 1)

        FBSbar.update(1)
    print('Calculating Win Quality:')
    FBSbar2 = tqdm(total=len(FBSteams))
    for key in FBSdict:
        FBSbar2.set_description(key)
        for w in range(4,curWeek+1):
            FBSdict[key]['win_q_'+str(w)] = FBSdict[key].apply(lambda row: winQ(row, w, FBSdict),axis=1)
        FBSbar2.update()
    print('Calculating PCT score:')
    FBSbar3 = tqdm(total=len(FBSteams))
    FBSpct = {}
    for key in FBSdict:
        FBSbar3.set_description(key)
        pctList = []
        for w in range(4,curWeek+1):
            pctList.append(calcPct(key,w,FBSdict))
        FBSpct[key] = pctList
        FBSbar3.update()

    if not os.path.exists(str(year)):
            os.mkdir(str(year))

    PCTdf = pd.DataFrame.from_dict(FBSpct,orient='index',columns=range(4,curWeek+1))
    PCTdf.to_csv('%s/PCT.csv'%year)

    PCTnormdf = pd.DataFrame(index = FBSteams,columns=range(4,curWeek+1))

    for w in range(4,curWeek+1):
        x = PCTdf[w].values.reshape(-1,1)
        min_max_scaler = preprocessing.MinMaxScaler()
        xScaled = min_max_scaler.fit_transform(x)
        PCTnormdf[w] = xScaled.reshape(len(FBSteams))

    PCTnormdf.to_csv('%s/PCT_norm.csv'%year)

    Ranks = PCTdf.rank(method='first',ascending=False).astype('int64')
    Ranks.to_csv('%s/Ranks.csv'%year)

    for w in range(4,curWeek+1):
        Wdf = pd.concat([PCTnormdf[w],Ranks[w]],axis=1)
        Wdf.columns = ['PCT','Rank']
        Wdf = Wdf.sort_values('Rank')
        Wdf.to_csv('%s/W%s.csv'%(year,w))
        
def plotTeamRank(team,teamInfo,Ranks,year,show=False):
    plt.figure(figsize=(12,5),facecolor='w')
    # plt.subplot(121)
    plt.gca().invert_yaxis()
    plt.title(team,size=18,fontweight='bold')
#     plt.title('Rankings over the 2019 CFB Season',size=14)
    plt.xlabel('Week',weight='medium')
    plt.ylabel('Rank',weight='medium')
    plt.xticks(fontname = 'NovaMono',weight='medium')
    plt.yticks(fontname = 'NovaMono',weight='medium')
    teamColor = teamInfo[teamInfo.school == team].color.item()
    teamAltColor = teamInfo[teamInfo.school == team].alt_color.item()
    plt.plot(Ranks.loc[team],c=teamColor,label=team,lw=5,
             marker = 'o',markersize=10,markerfacecolor=teamAltColor,markeredgewidth=2.5,markeredgecolor=teamColor)
    plt.tight_layout()
    if not os.path.exists(str(year)+'/Rank Graphs'):
            os.mkdir(str(year)+'/Rank Graphs')
    plt.savefig('%s/Rank Graphs/%s_%s_Ranks.png'%(year,team,year))
    if show:
        plt.show()
    else:
        plt.close()

def graphRanks(year):
    info_json_url = urllib.request.urlopen('https://api.collegefootballdata.com/teams/fbs?year=%s'%year)
    teamInfo = json.loads(info_json_url.read())
    teamInfo = pd.DataFrame(teamInfo)

    Ranks = pd.read_csv('%s/Ranks.csv'%year,index_col=0)
    PCT = pd.read_csv('%s/PCT.csv'%year,index_col=0)

    Ranks = Ranks.sort_values(str(max([int(r) for r in Ranks.columns])))

    TeamList = Ranks.index

    plt.rcParams['font.family'] = 'Roboto Mono'
    plt.rcParams['font.weight'] = 'medium'

    graphBar = tqdm(total=len(TeamList))
    print("Graphing:")
    for team in TeamList:
        graphBar.set_description(team)
        plotTeamRank(team,teamInfo,Ranks,year)
        graphBar.update(1)
        
    plt.figure(figsize=(12,7),facecolor='w')
    # plt.subplot(121)
    plt.gca().invert_yaxis()
    plt.title('Top Ten Teams',size=18,fontweight='bold')
    # plt.title('Rankings over the 2019 CFB Season',size=14)
    plt.xlabel('Week',weight='medium')
    plt.ylabel('Rank',weight='medium')
    plt.xticks(fontname = 'NovaMono',weight='medium')
    plt.yticks(fontname = 'NovaMono',weight='medium')
    teamColor = teamInfo[teamInfo.school == team].color.item()
    for team in TeamList[:10]:
        teamColor = teamInfo[teamInfo.school == team].color.item()
        teamAltColor = teamInfo[teamInfo.school == team].alt_color.item()
        plt.plot(Ranks.loc[team],c=teamColor,label=team,lw=5,
                 marker = 'o',markersize=10,markerfacecolor=teamAltColor,markeredgewidth=2.5,markeredgecolor=teamColor)
    plt.legend(bbox_to_anchor=(1, 1.025), loc='upper left', ncol=1)
    plt.tight_layout()
    plt.savefig('%s/topten.png'%year)
    plt.close()

    plt.figure(figsize=(12,8),facecolor='w')
    # plt.subplot(121)
    plt.gca().invert_yaxis()
    plt.title('Numbers 10 through 25',size=18,fontweight='bold')
    # plt.title('Rankings over the 2019 CFB Season',size=14)
    plt.xlabel('Week',weight='medium')
    plt.ylabel('Rank',weight='medium')
    plt.xticks(fontname = 'NovaMono',weight='medium')
    plt.yticks(fontname = 'NovaMono',weight='medium')
    teamColor = teamInfo[teamInfo.school == team].color.item()
    for team in TeamList[10:25]:
        teamColor = teamInfo[teamInfo.school == team].color.item()
        teamAltColor = teamInfo[teamInfo.school == team].alt_color.item()
        plt.plot(Ranks.loc[team],c=teamColor,label=team,lw=5,
                 marker = 'o',markersize=10,markerfacecolor=teamAltColor,markeredgewidth=2.5,markeredgecolor=teamColor)
    plt.legend(bbox_to_anchor=(1, 1.025), loc='upper left', ncol=1)
    plt.close()

    totalRise = Ranks['4'] - Ranks['15']
    totalRise = totalRise.sort_values()
    biggestRises = totalRise.tail(5)
    biggestFalls = totalRise.head(5)

    plt.figure(figsize=(12,5),facecolor='w')
    # plt.subplot(121)
    plt.gca().invert_yaxis()
    plt.title('Biggest Risers',size=18,fontweight='bold')
    # plt.title('Rankings over the 2019 CFB Season',size=14)
    plt.xlabel('Week',weight='medium')
    plt.ylabel('Rank',weight='medium')
    plt.xticks(fontname = 'NovaMono',weight='medium')
    plt.yticks(fontname = 'NovaMono',weight='medium')
    teamColor = teamInfo[teamInfo.school == team].color.item()
    for team in biggestRises.index:
        teamColor = teamInfo[teamInfo.school == team].color.item()
        teamAltColor = teamInfo[teamInfo.school == team].alt_color.item()
        plt.plot(Ranks.loc[team],c=teamColor,label=team,lw=5,
                 marker = 'o',markersize=10,markerfacecolor=teamAltColor,markeredgewidth=2.5,markeredgecolor=teamColor)
    plt.legend(bbox_to_anchor=(1, 1.025), loc='upper left', ncol=1)
    plt.tight_layout()
    plt.savefig('%s/risers.png'%year)
    plt.close()