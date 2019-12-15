import json
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
# import time
# import datetime

# start = time.time()

# POPULATE A LIST OF ESPN ID NUMBERS FOR FBS TEAMS
def get_ids():
    url = 'http://www.espn.com/college-football/teams'
    page = requests.get(url)

    soup = BeautifulSoup(page.text,'html.parser')

    id_list = []

    conf_list = soup.find_all('div',{'class':'mt7'})

    for conf in conf_list:
        conf_name = conf.find(class_ = 'headline ph0 clr-gray-05 h4').string
        conf_links = conf.find_all('a')
        for link in conf_links:
            if link.string == 'Schedule':
                team_name = conf_links[conf_links.index(link)-2].string
                team_id = link.get('href').split('/')[-1]
                id_list.append({'team':team_name,'id':team_id,'conf':conf_name})

    with open('id_list.json','w') as fout:
        json.dump(id_list,fout)

# test_list = get_ids()

def get_team(team):
    team_name = team['team']
    team_id = team['id']
    team_conf = team['conf']

    url = 'http://www.espn.com/college-football/team/schedule/_/id/' + str(team_id)
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    team_sch_table = soup.find(class_ = 'mod-content')
    team_sch_rows = team_sch_table.find_all('tr')

    team_sch_list = []

    #loop:
    for n in range(2,len(team_sch_rows)):
        try:
            #Néed to make a list of dictionaries
            thisweek = {}
            #convert variables to dictionary entries
            if len(team_sch_rows) == 15 and team_id != 2426:
                week = n - 2
            else:
                week = n - 1

            thisweek['week'] = week

            # print(week)

            opp_id = team_sch_rows[n].find_all('a')[1].get('href').split('/')[-2]
            thisweek['opp_id'] = opp_id

            opponent = team_sch_rows[n].find_all('li',{'class':'team-name'})
            opp_name = opponent[0].text

            score = team_sch_rows[n].find_all('li',{'class':'score'})
            if score[0].text == 'Canceled':
#                print('canceled')
                continue
            else: scores = score[0].text.strip(' ').strip(' OT').split('-')
            # print(scores)

            game_status = team_sch_rows[n].find_all('li',{'class':'game-status'})

            if opp_name[-1] == '*':
                location = 'N'
            else:
                location = game_status[0].string

            thisweek['loc'] = location

            result = game_status[1].string

            if result == 'W':
                team_score = scores[0]
                opp_score = scores[1]
                thisweek['result'] = result
            elif result == 'L':
                team_score = scores[1]
                opp_score = scores[0]
                thisweek['result'] = result
            else:
                continue
            score_diff = int(team_score) - int(opp_score)
            thisweek['team_score'] = team_score
            thisweek['opp_score'] = opp_score
            thisweek['score_diff'] = score_diff

            record = team_sch_rows[n].find_all('td')[-1].string.split(' ')[0]
            wins = record.split('-')[0]
            losses = record.split('-')[1]
            rawwinpct = float(wins)/(float(wins)+float(losses))
            thisweek['wins'] = wins
            thisweek['losses'] = losses
            thisweek['rawwinpct'] = rawwinpct
            team_sch_list.append(thisweek)
        except IndexError:
            team_sch_list.append(thisweek)
            break
    cur_rawwinpct = team_sch_list[-2]['rawwinpct']
    return team_sch_list, cur_rawwinpct


# Opening JSON list
with open('id_list.json') as json_data:
    team_list = json.load(json_data)

# FBS Splitting
P5_conf = ['ACC', 'Big 12', 'Big Ten', 'Pac-12', 'SEC']
G5_conf = ['Conference USA', 'Mid-American','Mountain West', 'Sun Belt']
AAC_conf = ['American Athletic']
Ind_conf = ['FBS Independents']

# Creating seperate lists for each division
mega_list = []
p5_list = []
g5_list = []
aac_list = []
fcs_list = []

j = 1
# pbar = tqdm(total=len(team_list))
for team in team_list:
    # pbar.write('Getting Data for',team['team'])
    print('\n('+str(j)+'/'+str(len(team_list))+')\nGetting Data for',team['team'])
    got_team = get_team(team)
    current = {}
    current['Name'] = team['team']
    current['ID'] = team['id']
    current['Conf'] = team['conf']
    current['Results'] = got_team[0]
    current['Raw Win Pct'] = got_team[1]

    if current['Conf'] in P5_conf:
        p5_list.append(current)
    elif current['Conf'] in G5_conf:
        g5_list.append(current)
    elif current['Conf'] in AAC_conf:
        aac_list.append(current)
    elif current['Conf'] in Ind_conf and current['ID'] == '87':
        p5_list.append(current)
    else:
        g5_list.append(current)

    mega_list.append(current)
    # pbar.write('Done')
    # pbar.update(1)
    j = j + 1
    print('\tDone')

fbs_list = p5_list + g5_list
p5_teams = [team['ID'] for team in p5_list]
aac_teams = [team['ID'] for team in aac_list]
g5_teams = [team['ID'] for team in g5_list]
fcs_teams = [team['ID'] for team in fcs_list]

with open('savefile.json','w') as fout:
    json.dump(mega_list,fout)
#
# with open('savefile.json','w') as fout:
#     json.dump(mega_list,fout)

with open('p5_teams.json','w') as fout:
    json.dump(p5_teams,fout)

with open('aac_teams.json','w') as fout:
    json.dump(aac_teams,fout)

with open('g5_teams.json','w') as fout:
    json.dump(g5_teams,fout)

with open('fcs_teams.json','w') as fout:
    json.dump(fcs_teams,fout)
