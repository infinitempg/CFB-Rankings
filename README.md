# Makmur CFB Rankings
*A ranking system based on win quality, opponent strength, and season progression*

This ranking system takes inspiration from [Devin Young](http://www.devinyoungweb.com/blog/cfb-rankings-the-right-way).

## Current Top 25
*Updated as of 9/25/2018*
See full rankings [here](https://github.com/infinitempg/CFB-Rankings/blob/master/Rankings_75_W5.md)

| #  | Team                       | Conf              | PCT   | W | L |
|----|----------------------------|-------------------|-------|---|---|
| 1  | Alabama Crimson Tide       | SEC               | 1.000 | 4 | 0 |
| 2  | Notre Dame Fighting Irish  | FBS Independents  | 0.835 | 4 | 0 |
| 3  | Georgia Bulldogs           | SEC               | 0.826 | 4 | 0 |
| 4  | Penn State Nittany Lions   | Big Ten           | 0.817 | 4 | 0 |
| 5  | Kentucky Wildcats          | SEC               | 0.813 | 4 | 0 |
| 6  | LSU Tigers                 | SEC               | 0.812 | 4 | 0 |
| 7  | Stanford Cardinal          | Pac-12            | 0.792 | 4 | 0 |
| 8  | Ohio State Buckeyes        | Big Ten           | 0.739 | 4 | 0 |
| 9  | West Virginia Mountaineers | Big 12            | 0.739 | 3 | 0 |
| 10 | Duke Blue Devils           | ACC               | 0.729 | 4 | 0 |
| 11 | Clemson Tigers             | ACC               | 0.699 | 4 | 0 |
| 12 | Texas Tech Red Raiders     | Big 12            | 0.688 | 3 | 1 |
| 13 | Syracuse Orange            | ACC               | 0.672 | 4 | 0 |
| 14 | Maryland Terrapins         | Big Ten           | 0.670 | 3 | 1 |
| 15 | South Florida Bulls        | American Athletic | 0.667 | 4 | 0 |
| 16 | Wisconsin Badgers          | Big Ten           | 0.660 | 3 | 1 |
| 17 | South Carolina Gamecocks   | SEC               | 0.654 | 2 | 1 |
| 18 | Buffalo Bulls              | Mid-American      | 0.650 | 4 | 0 |
| 19 | Texas Longhorns            | Big 12            | 0.646 | 3 | 1 |
| 20 | Oklahoma Sooners           | Big 12            | 0.643 | 4 | 0 |
| 21 | BYU Cougars                | FBS Independents  | 0.632 | 3 | 1 |
| 22 | Washington Huskies         | Pac-12            | 0.632 | 3 | 1 |
| 23 | North Texas Mean Green     | Conference USA    | 0.607 | 4 | 0 |
| 24 | California Golden Bears    | Pac-12            | 0.600 | 3 | 0 |
| 25 | Auburn Tigers              | SEC               | 0.594 | 3 | 1 |

## Files

* id_list.json: A JSON that matches all FBS teams to their ESPN ID
* rankings.py: Obtains team, schedule, and result information from ESPN, and saves these in a JSON file.
* savefile.json: A JSON file containing all information gathered from rankings.py
* division_teams.json: A JSON file containing a list of teams in the specified conference/division
* ranker.py: Calculates the overall PCT based on win quality, record, etc. described below.
* rankings_\*.xlsx: Contains the rankings (where the \* is the AAC multiplier) throughout the season.

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

Neutral games are treated as home games.

## To-Do List
* Analysis of ranking progression from Week 4 to present, creating interactive graphs for each team and allowing comparison of teams
* Clean up code and add comments
