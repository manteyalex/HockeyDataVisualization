# HockeyDataVisualization
Visualization tool for hockey data from https://github.com/bigdatacup/Big-Data-Cup-2021 developed using Python 3.8    
Install libraries from requirements.txt  
Then run using HockeyDataApplication.py  
 
When first opening the tool the interface shows the rink plot and data tables. A data file needs to be loaded by either:    
clicking File -> Load Data File  
Or by pressing ctrl+o.

![alt text](https://github.com/manteyalex/HockeyDataVisualization/blob/main/Screenshots/Team%20Selection.png?raw=true)

Once loaded, a team can be selected in the Team drop-down box. This allows the user to focus on a particular team and look at information related to their shots and goals.  
Once selected, that team's games will now appear in the Game drop-down box.  

![alt text](https://github.com/manteyalex/HockeyDataVisualization/blob/main/Screenshots/Team%20Selection.png?raw=true)

Next, one or more games can be selected to view information related to that teams's shots and goals, as well as their opposition. In the main rink plot shots and goals are displayed at their locations, and a heatmap is plotted to observe locations with relatively high or low shot counts. Tables are made showing the goal and shot counts by period, and another table is made showing more detailed shot information.  

The left side and red colour always represents the selected team's shots and goals, while the right side and blue colour always represents the selected team's opposition's shots and goals.  

When a single game is selected you can use this information to assess a team's ability to attack and defend in that game.  

![alt text](https://github.com/manteyalex/HockeyDataVisualization/blob/main/Screenshots/Game%20Selection.png?raw=true)  

When multiple games are selected you can use this information to assess a team's ability to attack and defend in the aggregate against one or more opponents.  

![alt text](https://github.com/manteyalex/HockeyDataVisualization/blob/main/Screenshots/Game%20Selection%20Multiple%20Games.png?raw=true)  
