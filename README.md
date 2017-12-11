# Makmur CFB Rankings
*A ranking system based on win quality, opponent strength, and season progression*

This ranking system takes inspiration from [Devin Young](http://www.devinyoungweb.com/blog/cfb-rankings-the-right-way).

## Current Top 25
*Updated as of 12/10/17*

**#**|**Team**|**Conf**|**PCT**|**W**|**L**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
1|Clemson|Atlantic Coast Conference|1.000|12|1
2|Georgia|Southeastern Conference|0.997|12|1
3|Oklahoma|Big 12 Conference|0.969|12|1
4|Wisconsin|Big Ten Conference|0.926|12|1
5|Alabama|Southeastern Conference|0.919|11|1
6|Ohio State|Big Ten Conference|0.917|11|2
7|UCF|American Athletic Conference|0.880|12|0
8|USC|Pac-12 Conference|0.871|11|2
9|Penn State|Big Ten Conference|0.855|10|2
10|Auburn|Southeastern Conference|0.849|10|3
11|Washington|Pac-12 Conference|0.822|10|2
12|Miami (Fla.)|Atlantic Coast Conference|0.820|10|2
13|Notre Dame|FBS Independent|0.790|9|3
14|TCU|Big 12 Conference|0.753|10|3
15|Stanford|Pac-12 Conference|0.750|9|4
16|LSU|Southeastern Conference|0.749|9|3
17|Michigan State|Big Ten Conference|0.745|9|3
18|Northwestern|Big Ten Conference|0.737|9|3
19|Memphis|American Athletic Conference|0.729|10|2
20|Troy|Sun Belt Conference|0.724|10|2
21|Florida Atlantic|Conference USA|0.715|10|3
22|Virginia Tech|Atlantic Coast Conference|0.714|9|3
23|San Diego State|Mountain West Conference|0.707|10|2
24|Oklahoma State|Big 12 Conference|0.703|9|3
25|Washington State|Pac-12 Conference|0.698|9|3

## Files

* d1_school.json: A JSON (modified from Devin Young's list) of all D1 (FBS/FCS) schools, linking their names on the NCAA.com website and their URLs
* rankings.py: Obtains team, schedule, and result information from the NCAA.com website, and saves these in a JSON file.
* savefile.json: A JSON file containing all information gathered from rankings.py
* (division)_teams.json: A JSON file containing a list of teams in the specified conference/division
* ranker.py: Calculates the overall PCT based on win quality, record, etc. described below.
* testgraph.py: (WIP) Creates interactive graphs for each team

## Calculations

The [formula for PCT](/Images/Eqs/Raw_Pct.png "Raw Percentage Formula") is based on a combination of win quality (described more below) and the team's current record (taking into account the number of games played). It is then [normalized to a 0-1 scale](Images/Eqs/Norm_Pct.png "Normalized Percentage").

### Win Quality

The win quality statistic is meant to give wins against good teams more value than wins against bad teams, and vice versa for losses. The first part of the win quality is a straight +/- 1 point for a win/loss, respectively. The location is then taken into account, with an extra +0.1 points added for an away victory or an extra -0.1 points removed for a home loss. This number is then added by a multiplier for score difference, with +/- 0.01 for each point in the score difference.

Next, this is multiplied by the *current* win/loss percentage of the opponent. A win against a (2-7) team does not have as much benefit as a win against a (6-3) team, and a loss against a (2-7) team hurts more than a loss to a (6-3) team.

Next, this is multiplied by a different number depending on the conference/division the opponent plays in:

* 1.0x for a team in the P5 (or Notre Dame)
* 0.5x for a team in the G5 (or FBS Independents)
* 0.15x for a team in the FCS

There is also a provision to change the multiplier for teams in the AAC (#POW6R).

Lastly, the win quality is multiplied by a [season progression factor](/Images/Eqs/Season_Multiplier.png "Season Multiplier"). This helps shift weight towards more recent results, punishing harshly for late-season losses and being more lenient on early-season losses.

The final formula:
* [Home Win](/Images/Eqs/WQ_HW.png "Home Win")
* [Home Loss](/Images/Eqs/WQ_HL.png "Home Loss")
* [Away Win](/Images/Eqs/WQ_AW.png "Away Win")
* [Away Loss](/Images/Eqs/WQ_AL.png "Away Loss")

## Analysis

As mentioned above, there is a provision to rate the AAC with a higher multiplier than other G5 teams. This would put UCF up to #4 in the rankings (and thus a theoretical playoff spot). There are also a lot more G5 teams represented in this ranking system than in the CFP Committee's rankings (which as we know has a strong bias against G5 teams). Lastly, this ranking system completely forgoes the Alabama/OSU 4th place fight by keeping Wisconsin in that slot, which I may not necessarily agree with.

## To-Do List
* Analysis of ranking progression from Week 4 to present, creating interactive graphs for each team and allowing comparison of teams
* Determining how neutral games are worked
