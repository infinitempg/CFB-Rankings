# Makmur CFB Rankings
*A ranking system based on win quality, opponent strength, and season progression*

**This has been updated in 2019.**

This ranking system takes inspiration from [Devin Young](http://www.devinyoungweb.com/blog/cfb-rankings-the-right-way).

The data has been pulled from [collegefootballdata.com](https://collegefootballdata.com/). Thanks /u/BlueSCar from /r/CFBAnalysis!

## Current Top 25
| Rank | Team              | PCT   | Record |
|------|-------------------|-------|--------|
| 1    | LSU               | 1.0   | (15-0) |
| 2    | Clemson           | 0.869 | (14-1) |
| 3    | Ohio State        | 0.831 | (13-1) |
| 4    | Georgia           | 0.775 | (12-2) |
| 5    | Oregon            | 0.763 | (12-2) |
| 6    | Oklahoma          | 0.743 | (12-2) |
| 7    | Notre Dame        | 0.723 | (11-2) |
| 8    | Appalachian State | 0.705 | (13-1) |
| 9    | Florida           | 0.691 | (11-2) |
| 10   | Penn State        | 0.685 | (11-2) |
| 11   | Alabama           | 0.666 | (11-2) |
| 12   | Minnesota         | 0.657 | (11-2) |
| 13   | Utah              | 0.643 | (11-3) |
| 14   | Memphis           | 0.641 | (12-2) |
| 15   | Navy              | 0.639 | (11-2) |
| 16   | Iowa              | 0.63  | (10-3) |
| 17   | Air Force         | 0.63  | (11-2) |
| 18   | Baylor            | 0.625 | (11-3) |
| 19   | Boise State       | 0.621 | (12-2) |
| 20   | Florida Atlantic  | 0.61  | (11-3) |
| 21   | Wisconsin         | 0.603 | (10-4) |
| 22   | Cincinnati        | 0.592 | (11-3) |
| 23   | Michigan          | 0.585 | (9-4)  |
| 24   | Louisiana         | 0.582 | (11-3) |
| 25   | UCF               | 0.544 | (10-3) |

## Historical Rankings

You can view rankings (in this system) for all seasons from 1990 to the present! There are also graphs describing each team's rank and score throughout the last 30 years.

## Calculations

The [formula for PCT](/Images/Eqs/Raw_Pct.png "Raw Percentage Formula") is based on a combination of win quality (described more below) and the team's current record (taking into account the number of games played). It is then normalized to a 0-1 scale. *Of note: I changed the multiplier for Wins/Losses from 0.025 to 0.01.*

### Win Quality

The win quality statistic is meant to give wins against good teams more value than wins against bad teams, and vice versa for losses. The first part of the win quality is a straight +/- 1 point for a win/loss, respectively. The location is then taken into account, with an extra +0.1 points added for an away victory or an extra -0.1 points removed for a home loss. This number is then added by a multiplier for score difference, with +/- 0.01 for each point in the score difference.

Next, this is multiplied by the *current* win/loss percentage of the opponent. A win against a (2-7) team does not have as much benefit as a win against a (6-3) team, and a loss against a (2-7) team hurts more than a loss to a (6-3) team. *Of note: the win/loss percentage of FCS opponents is automatically set to 100%. The conference multiplier (coming next) is harsh enough already.*

Next, this is multiplied by a different number depending on the conference/division the opponent plays in:

* 1.0x for a team in the P5 (or Notre Dame)
* 0.5x for a team in the G5 (or FBS Independents)
* 0.15x for a team in the FCS

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

Neutral games are given a multiplier of 1.05.
