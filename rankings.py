import json
from bs4 import BeautifulSoup
import requests
import time
import datetime

start = time.time()

# Obtain Schedule information
def get_team(teamurl):
    url = "http://www.ncaa.com/schools/" + teamurl + "/football"
    page = requests.get(url)

    soup = BeautifulSoup(page.text,'html.parser')

    school_div = soup.find(class_= 'school-info').contents[-1][1:]
    school_conf = soup.findAll(class_= 'school-info')[1].contents[-1][1:]

    team_game_list = soup.find(class_='ncaa-schools-sport-table')
    team_game_list_items = team_game_list.find_all('td')

    teamsch = []
    n = 0
    while n < len(team_game_list_items):
        thisweek = {}
        gamedate = team_game_list_items[n].contents[0]
        thisweek['date'] = gamedate
        if team_game_list_items[n+1].contents[0] == '@ ':
            loc = 'A'
        else:
            loc = 'H'
        thisweek['loc'] = loc
        if team_game_list_items[n+1].contents[-1] == '*':
            opp = team_game_list_items[n+1].contents[-2]
            opp = opp.contents[0]
        else:
            opp = team_game_list_items[n+1].contents[-1]
            opp = opp.contents[0]
        if ' St.' in opp:
            opp = opp.replace(' St.', ' State')
        if 'State ' in opp:
            opp = opp.replace('State ','State')
        if opp == 'Mich. State':
            opp = opp.replace('Mich.','Michigan')
        if opp == 'Louisiana':
            opp = 'La.-Lafayette'
        thisweek['opp'] = opp.strip(';')
        try:
            result = team_game_list_items[n+2].contents[0]
        except IndexError:
            teamsch.append(thisweek)
            break
        wl = result[0]
        thisweek['result'] = wl
        score = result[2:].split('-')
        if wl == 'W':
            teamscore = score[0]
            oppscore = score[1]
        elif wl == 'L':
            teamscore = score[1]
            oppscore = score[0]
        thisweek['teamscore'] = teamscore
        thisweek['oppscore'] = oppscore
        thisweek['score_diff'] = int(teamscore) - int(oppscore)
        record = team_game_list_items[n+3].contents[0].strip('(').strip(')').split('-')
        win = record[0]
        loss = record[1]
        thisweek['wins'] = win
        thisweek['losses'] = loss
        teamsch.append(thisweek)
        n = n + 4
    try:
        currec = team_game_list_items[n-1].contents[0].strip('(').strip(')').split('-')
        raw_winpct = (float(currec[0]))/(float(currec[1])+float(currec[0]))
    except IndexError:
        currec = 0
        raw_winpct = 0
    return teamsch, raw_winpct, school_div, school_conf

# Opens the JSON file that connects name to URL
with open('d1school.json') as json_data:
    team_list = json.load(json_data)

# Defining FBS Split
P5_conf = ['Atlantic Coast Conference','Big Ten Conference','Big 12 Conference','Southeastern Conference','Pac-12 Conference']
G5_conf = ['Conference USA','Mid-American Conference','Mountain West Conference','Sun Belt Conference']
AAC_conf = ['American Athletic Conference']

# Creating seperate lists for each division
mega_list = []
p5_list = []
g5_list = []
aac_list = []
fcs_list = []

j = 1
for team in team_list:
    print('\n('+str(j)+'/'+str(len(team_list))+')\nGetting Data for',team['name'])
    got_team = get_team(team['url'])
    current = {}
    current['Name'] = team['name']
    current['Div'] = got_team[2]
    current['Conf'] = got_team[3]
    current['Results'] = got_team[0]
    current['Raw Win Pct'] = got_team[1]
    # Splitting into Divisions
    if current['Div'] == 'Div FBS':
        if current['Conf'] in P5_conf:
            p5_list.append(current)
            mega_list.append(current)
        elif current['Conf'] in G5_conf:
            g5_list.append(current)
            mega_list.append(current)
        elif current['Conf'] == 'American Athletic Conference':
            aac_list.append(current)
            mega_list.append(current)
        elif current['Conf'] == 'FBS Independents' and current['Name'] == 'Notre Dame':
            p5_list.append(current)
            mega_list.append(current)
        else:
            g5_list.append(current)
            mega_list.append(current)
    elif current['Div'] == 'Div FCS':
        fcs_list.append(current)
        mega_list.append(current)
    j = j + 1
    print('\tDone')

fbs_list = p5_list + g5_list
p5_teams = [team['Name'] for team in p5_list]
aac_teams = [team['Name'] for team in aac_list]
g5_teams = [team['Name'] for team in g5_list]
fcs_teams = [team['Name'] for team in fcs_list]

with open('savefile.json','w') as fout:
    json.dump(mega_list,fout)

with open('savefile.json','w') as fout:
    json.dump(mega_list,fout)

with open('p5_teams.json','w') as fout:
    json.dump(p5_teams,fout)

with open('aac_teams.json','w') as fout:
    json.dump(aac_teams,fout)

with open('g5_teams.json','w') as fout:
    json.dump(g5_teams,fout)

with open('fcs_teams.json','w') as fout:
    json.dump(fcs_teams,fout)

end = time.time()
print(end - start,'s')
