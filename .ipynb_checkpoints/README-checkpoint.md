# Makmur CFB Rankings
*A ranking system based on win quality, opponent strength, and season progression*

**This has been updated in 2020.**

This ranking system takes inspiration from [Devin Young](http://www.devinyoungweb.com/blog/cfb-rankings-the-right-way).

The data has been pulled from [collegefootballdata.com](https://collegefootballdata.com/). Thanks /u/BlueSCar from /r/CFBAnalysis!

## Current Top 25
WEEK 9, 2020 RANKINGS
Ranking teams who have played at least 4 games.

|   Rank | Team             |   PCT | Record   |
|--------|------------------|-------|----------|
|      1 | Alabama          | 1.000 | (6-0)    |
|      2 | Clemson          | 0.917 | (7-0)    |
|      3 | Notre Dame       | 0.799 | (6-0)    |
|      4 | Cincinnati       | 0.777 | (5-0)    |
|      5 | Georgia          | 0.772 | (4-1)    |
|      6 | Coastal Carolina | 0.738 | (6-0)    |
|      7 | Texas A&M        | 0.726 | (4-1)    |
|      8 | BYU              | 0.725 | (7-0)    |
|      9 | Marshall         | 0.698 | (5-0)    |
|     10 | Miami            | 0.690 | (5-1)    |
|     11 | Florida          | 0.671 | (3-1)    |
|     12 | Wake Forest      | 0.649 | (4-2)    |
|     13 | Oklahoma         | 0.632 | (4-2)    |
|     14 | Oklahoma State   | 0.631 | (4-1)    |
|     15 | Virginia Tech    | 0.619 | (4-2)    |
|     16 | SMU              | 0.619 | (6-1)    |
|     17 | Louisiana        | 0.613 | (5-1)    |
|     18 | Auburn           | 0.597 | (4-2)    |
|     19 | Texas            | 0.584 | (4-2)    |
|     20 | Liberty          | 0.579 | (6-0)    |
|     21 | Army             | 0.571 | (6-1)    |
|     22 | Iowa State       | 0.567 | (4-2)    |
|     23 | NC State         | 0.563 | (4-2)    |
|     24 | North Carolina   | 0.542 | (4-2)    |
|     25 | Tulsa            | 0.539 | (3-1)    |

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
