from operator import itemgetter
import datetime
import csv

def index(name):
    for team in mega_list:
        if team['Name'] == name:
            return mega_list.index(team)

def enter_game(teamname,game_num,result,teamscore,oppscore,wins,losses):
    i = index(teamname)
    mega_list[i]['Results'][game_num]['result'] = result
    mega_list[i]['Results'][game_num]['teamscore'] = str(teamscore)
    mega_list[i]['Results'][game_num]['oppscore'] = str(oppscore)
    mega_list[i]['Results'][game_num]['score_diff'] = int(teamscore) - int(oppscore)
    mega_list[i]['Results'][game_num]['wins'] = str(wins)
    mega_list[i]['Results'][game_num]['losses'] = str(losses)

enter_game('Army West Point',-1,'W','14','13','9','3')
enter_game('Navy',-1,'L','13','14','6','6')

def deleteaboveweek(dateofweek):
    for team in mega_list:
        for n in range(len(team['Results'])-1,-1,-1):
            if team['Results'][n]['Date'] >= dateofweek:
                del team['Results'][n]
    return mega_list

def get_ranks(mega_list,weeknum):
    for team in mega_list:
        win_q_list = []
        try:
            team['Record'] = [team['Results'][-1]['wins'],team['Results'][-1]['losses']]
        except KeyError:
            team['Record'] = [team['Results'][-2]['wins'],team['Results'][-2]['losses']]
        except IndexError:
            team['Record'] = [0,0]
            continue
        loss_ct = 0
        win_ct = 0
        game_ct = 1
        for game in team['Results']:  
            divmult = 0
            if game['opp'] in p5_teams:
                divmult = 1.0
            elif game['opp'] in aac_teams:
                divmult = 0.5
            elif game['opp'] in g5_teams:
                divmult = 0.5
            elif game['opp'] in fcs_teams:
                divmult = 0.15
            if game['opp'] == 'Notre Dame':
                divmult = 1.0
            game['divmult'] = divmult
            result_pts = 0.0
            try:
                if game['result'] == 'W':
                    result_pts = 1.0
                    win_ct = win_ct + 1
                    if game['loc'] == 'A':
                        result_pts = result_pts + 0.1
                elif game['result'] == 'L':
                    result_pts = -1.0
                    loss_ct = loss_ct + 1
                    if game['loc'] == 'H':
                        result_pts = result_pts - 0.1
            except KeyError:
                break
            game['result_pts'] = result_pts
            oppwinpct = 0
            for school in mega_list:
                if school['Name'] == game['opp']:
                    if game['result'] == 'W':
                        oppwinpct = float(school['Raw Win Pct'])
                    if game['result'] == 'L':
                        oppwinpct = 1-float(school['Raw Win Pct'])
            game['oppwinpct'] = oppwinpct
            
            game_mult = game_ct/len(team['Results']) * 0.5 + 0.5
            
            win_q = (result_pts + 0.01*float(game['score_diff']))*divmult*oppwinpct*game_mult
            
            win_q_list.append(win_q)
            game['win_q'] = win_q
            game_ct = game_ct + 1
            
        team['PCT'] = (0.9*sum(win_q_list)/len(win_q_list) + 0.025*win_ct - 0.025*loss_ct)
            
    
    ranks = []
    fbs_rank_list = []
    for team in mega_list:
        if team['Div'] == 'Div FBS' and team['Name'] != 'Liberty':
            fbs_rank_list.append(team)
    
    raw_pct = []
    for team in fbs_rank_list:
        innerlist = []
        innerlist.append(team['Name'])
        innerlist.append(team['Conf'])
        innerlist.append(team['PCT'])
        raw_pct.append(team['PCT'])
        innerlist.append(team['Record'][0])
        innerlist.append(team['Record'][1])
        ranks.append(innerlist)
    
    for team in ranks:
        team[2] = (team[2] - min(raw_pct))/(max(raw_pct) - min(raw_pct))
    
    ranks = sorted(ranks,key=itemgetter(2),reverse=True)
    
    print('--------------- TOP 25 -------------------')
    for num in range(0,25):
        if num+1 < 10:
            numstr = ' ' + str(num+1)
        else:
            numstr = str(num+1)
        print(numstr+'.',str(ranks[num][0]),'('+str(ranks[num][3]+'-'+str(ranks[num][4]))+'),','PCT = %.2f'%(ranks[num][2]*100)+'%')
    
    print('------------------------------------------')
    
    myFile = open('rankings_w%s.csv'%str(weeknum+1),'w',newline='')
    myFile.write('Team,Conf,PCT,W,L\n')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(ranks)

dates = [datetime.date(2017, 9, 7),
 datetime.date(2017, 9, 14),
 datetime.date(2017, 9, 21),
 datetime.date(2017, 9, 28),
 datetime.date(2017, 10, 4),
 datetime.date(2017, 10, 11),
 datetime.date(2017, 10, 19),
 datetime.date(2017, 10, 26),
 datetime.date(2017, 10, 31),
 datetime.date(2017, 11, 7),
 datetime.date(2017, 11, 14),
 datetime.date(2017, 11, 21),
 datetime.date(2017, 12, 1),
 datetime.date(2017, 12, 9),
 datetime.date(2017, 12, 16)]

get_ranks(mega_list,16)

#for weeknum in range(16,2,-1):
#    print('WEEK %s RANKINGS'%str(weeknum+1),'('+str(dates[weeknum-2])+')')
#    get_ranks(mega_list,weeknum)
#    mega_list = deleteaboveweek(dates[weeknum-2])
#    

