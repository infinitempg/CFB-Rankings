# Makmur CFB Rankings
*A ranking system based on win quality, opponent strength, and season progression*

This ranking system takes inspiration from [Devin Young](http://www.devinyoungweb.com/blog/cfb-rankings-the-right-way).

## Current Top 25
*Updated as of 2/5/2018*

| **#** | **Team** | **Conf** | **PCT** | **W** | **L** |
|----|------------------|------------------------------|-------|----|---|
| 1 | Alabama | Southeastern Conference | 1.000 | 13 | 1 |
| 2 | Georgia | Southeastern Conference | 0.967 | 13 | 2 |
| 3 | Wisconsin | Big Ten Conference | 0.962 | 13 | 1 |
| 4 | Ohio State | Big Ten Conference | 0.948 | 12 | 2 |
| 5 | Clemson | Atlantic Coast Conference | 0.930 | 12 | 2 |
| 6 | UCF | American Athletic Conference | 0.917 | 13 | 0 |
| 7 | Oklahoma | Big 12 Conference | 0.908 | 12 | 2 |
| 8 | Penn State | Big Ten Conference | 0.891 | 11 | 2 |
| 9 | Notre Dame | FBS Independent | 0.818 | 10 | 3 |
| 10 | USC | Pac-12 Conference | 0.807 | 11 | 3 |
| 11 | Michigan State | Big Ten Conference | 0.794 | 10 | 3 |
| 12 | Auburn | Southeastern Conference | 0.788 | 10 | 4 |
| 13 | TCU | Big 12 Conference | 0.783 | 11 | 3 |
| 14 | Northwestern | Big Ten Conference | 0.774 | 10 | 3 |
| 15 | Miami (Fla.) | Atlantic Coast Conference | 0.766 | 10 | 3 |
| 16 | Washington | Pac-12 Conference | 0.759 | 10 | 3 |
| 17 | Troy | Sun Belt Conference | 0.751 | 11 | 2 |
| 18 | Oklahoma State | Big 12 Conference | 0.749 | 10 | 3 |
| 19 | Florida Atlantic | Conference USA | 0.738 | 11 | 3 |
| 20 | Boise State | Mountain West Conference | 0.726 | 11 | 3 |
| 21 | South Florida | American Athletic Conference | 0.704 | 10 | 2 |
| 22 | LSU | Southeastern Conference | 0.693 | 9 | 4 |
| 23 | NC State | Atlantic Coast Conference | 0.690 | 9 | 4 |
| 24 | Stanford | Pac-12 Conference | 0.685 | 9 | 5 |
| 25 | Army West Point | FBS Independent | 0.683 | 10 | 3 |

## Files

* d1_school.json: A JSON (modified from Devin Young's list) of all D1 (FBS/FCS) schools, linking their names on the NCAA.com website and their URLs
* rankings.py: Obtains team, schedule, and result information from the NCAA.com website, and saves these in a JSON file.
* savefile.json: A JSON file containing all information gathered from rankings.py
* division_teams.json: A JSON file containing a list of teams in the specified conference/division
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

Home Win:
![Home Win](/Images/Eqs/WQ_HW.png "Home Win")
Home Loss:
![Home Loss](/Images/Eqs/WQ_HL.png "Home Loss")
Away Win:
![Away Win](/Images/Eqs/WQ_AW.png "Away Win")
Away Loss:
![Away Loss](/Images/Eqs/WQ_AL.png "Away Loss")

## Analysis

As mentioned above, there is a provision to rate the AAC with a higher multiplier than other G5 teams. This higher multiplier puts UCF at #4 prior to the CFP, and at #2 overall after the bowl games (with Alabama at #1). There are also a lot more G5 teams represented in this ranking system than in the CFP Committee's rankings (which as we know has a strong bias against G5 teams). Lastly, this ranking system completely skipped the Alabama/OSU 4th place CFP fight by keeping Wisconsin in that slot, which I may not necessarily agree with.

## To-Do List
* Analysis of ranking progression from Week 4 to present, creating interactive graphs for each team and allowing comparison of teams
* Determining how neutral games are worked
* Clean up code and add comments
