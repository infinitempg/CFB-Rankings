# Makmur CFB Rankings
*A ranking system based on win quality, opponent strength, and season progression*

**This has been updated in 2019.**

This ranking system takes inspiration from [Devin Young](http://www.devinyoungweb.com/blog/cfb-rankings-the-right-way).

The data has been pulled from [collegefootballdata.com](https://collegefootballdata.com/). Thanks /u/BlueSCar from /r/CFBAnalysis!

## Files

* `CFB_rankings.ipynb` - The Jupyter notebook where the magic happens.
* `2019/2019schedule.json` - The JSON returned from [collegefootballdata.com](https://collegefootballdata.com) for all 2019 games. Does not include post season currently.
* `code_testing.ipynb` - A little playground for making sure things work.
* `old code` - Code used to generate 2018 and previous rankings.

Rankings from W4 to W15 of the 2019 season can be found in CSV format in the `2019` folder.

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

## Current Top 25
|Rank|TEAM                 |PCT  |
|----|---------------------|-----|
|1   |Ohio State           |1.000|
|2   |LSU                  |0.991|
|3   |Clemson              |0.971|
|4   |Oklahoma             |0.895|
|5   |Oregon               |0.814|
|6   |Georgia              |0.809|
|7   |Utah                 |0.780|
|8   |Notre Dame           |0.773|
|9   |Memphis              |0.766|
|10  |Baylor               |0.760|
|11  |Appalachian State    |0.760|
|12  |Boise State          |0.752|
|13  |Penn State           |0.735|
|14  |Wisconsin            |0.733|
|15  |Florida              |0.725|
|16  |Michigan             |0.713|
|17  |Alabama              |0.686|
|18  |Minnesota            |0.680|
|19  |Navy                 |0.663|
|20  |Air Force            |0.661|
|21  |Iowa                 |0.653|
|22  |Florida Atlantic     |0.648|
|23  |Auburn               |0.642|
|24  |SMU                  |0.636|
|25  |Cincinnati           |0.619|
