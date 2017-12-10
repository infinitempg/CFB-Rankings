import csv
#import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import Range1d
from bokeh.palettes import Spectral4
from bokeh.models import HoverTool

team_list = []
with open('rankings_50.csv', newline = '') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    csvfile.readline()
    for row in csvreader:
        team = {}
        team['Name'] = row[0]
        team['Ranks'] = row[1:]
        team_list.append(team)


weeks = [4,5,6,7,8,9,10,11,12,13,14,15]
teamname = [team['Name'] for team in team_list]
USAF = team_list[0]['Ranks'][:-1]

#source = ColumnDataSource(data=dict(
#        Week = [str(weeknum) for weeknum in weeks],
#        Rank = USAF,
#))

source = ColumnDataSource(data=dict(
    weeks = [4,5,6,7,8,9,10,11,12,13,14,15],
    ranks = team_list[0]['Ranks'][:-1],
#        desc=['A', 'b', 'C', 'd', 'E','f','g','h','i','j','k','l'],
))

p = figure(plot_width=800,plot_height=600,tools=[],title='Rank Progression')

p.xaxis.axis_label = 'Week'
p.yaxis.axis_label = 'Ranking'
p.y_range = Range1d(130,0)

dots = p.circle(weeks,USAF,size=20,legend=team_list[0]['Name'],color = Spectral4[0],source=source)
line = p.line(weeks,USAF,line_width=2,legend=team_list[0]['Name'],color = Spectral4[0])



hover = HoverTool(
        tooltips=[
                ("Team", teamname[0]),
                ("Week", "@weeks"),
                ('Rank', '@ranks'),
                ],
        renderers = [dots]
)
p.tools.append(hover)

rank15 = team_list[15]['Ranks'][:-1]
source2 = ColumnDataSource(data=dict(
    weeks = [4,5,6,7,8,9,10,11,12,13,14,15],
    ranks = team_list[15]['Ranks'][:-1],
#        desc=['A', 'b', 'C', 'd', 'E','f','g','h','i','j','k','l'],
))

dots2 = p.circle(weeks,rank15,size=20,legend=team_list[15]['Name'],color = Spectral4[1],source=source2)
line2 = p.line(weeks,rank15,line_width=2,legend=team_list[15]['Name'],color = Spectral4[1])
hover2 = HoverTool(
        tooltips=[
                ("Team", teamname[15]),
                ("Week", "@weeks"),
                ('Rank', '@ranks'),
                ],
        renderers = [dots2]
)
p.tools.append(hover2)

output_file('test.html')

p.legend.click_policy = 'hide'
show(p)