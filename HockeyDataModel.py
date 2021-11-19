import pandas as pd
from PyQt5 import QtCore
import numpy as np
class HockeyDataModel:
    def __init__(self):
        self.df = None
        self.recent_game = None
        self.recent_home_team = None
        self.games = []
        self.teams = []



    def load_data(self,filename):
        self.df = pd.read_csv(filename)
        self._get_data_for_ui()


    def _get_data_for_ui(self):
        self.games = list(self.df['game_date'].unique())
        self.teams = list(set(list(self.df['Home Team'].unique()) + list(self.df['Away Team'].unique()))) #set to remove duplicates
        self.games.sort(reverse=True)
        self.teams.sort()

        self.recent_game = self.games[0]
        self.recent_home_team = list(self.df[self.df['game_date'] == self.recent_game]['Home Team'])[0]

        return


    def _get_event_locations_single_game(self,events,game,filter_shots_on_net=True):
        game_data = self.df[self.df['game_date'] == game]
        assert len(game_data['Home Team'].unique()) == 1  # Maybe multiple games on one day?
        assert len(game_data['Away Team'].unique()) == 1  # Maybe multiple games on one day?
        home_team = list(game_data['Home Team'])[0]
        away_team = list(game_data['Away Team'])[0]

        home_team_events = game_data[game_data['Team'] == home_team]
        away_team_events = game_data[game_data['Team'] == away_team]


        # Set limits to coordinates for rink
        include_shots_on_net = False
        if filter_shots_on_net:
            if "Shot" in events:
                include_shots_on_net = True
                events.remove("Shot")
        home_events = home_team_events[home_team_events['Event'].isin(events)]
        away_events = away_team_events[away_team_events['Event'].isin(events)]

        if include_shots_on_net:
            home_shots = home_team_events[(home_team_events['Event'] == "Shot") & (home_team_events['Detail 2'] == "On Net")]
            home_events = home_events.append(home_shots)
            away_shots = away_team_events[(away_team_events['Event'] == "Shot") & (away_team_events['Detail 2'] == "On Net")]
            away_events = away_events.append(away_shots)

        return home_events, away_events

    def _distance_from_point_to_goal_line(self, x0, y0):
        # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        x1, y1 = 189, 45.5
        x2, y2 = 189, 39.5
        distance = np.abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / \
                   np.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance

    def get_team_games(self,team):
        df_team = self.df[(self.df['Home Team'] == team) | (self.df['Away Team'] == team)]
        df_team = df_team.sort_values(by='game_date', ascending=False)
        game_days = df_team['game_date'].unique()

        games = []

        for gd in game_days:
            single_row = df_team[df_team['game_date']==gd].iloc[0,:]
            home = single_row['Home Team']
            away = single_row['Away Team']
            joining_word = ' vs. ' if home == team else ' at '
            opposition = away if home == team else home
            games.append(gd+joining_word+opposition)



        return games


    def get_detailed_shot_information(self,focused_team,game):
        home, away = self._get_event_locations_single_game(['Goal', 'Shot'], game=game, filter_shots_on_net=False)
        home['Distance'] = home.apply(lambda x: self._distance_from_point_to_goal_line(x['X Coordinate'], x['Y Coordinate']),axis=1)
        away['Distance'] = away.apply(lambda x: self._distance_from_point_to_goal_line(x['X Coordinate'], x['Y Coordinate']),axis=1)
        ht = list(home['Home Team'])[0]
        at = list(away['Away Team'])[0]

        teams = {}
        home_event_counts = {}
        away_event_counts = {}

        home_event_counts['Shot Attempts'] = len(home)
        away_event_counts['Shot Attempts'] = len(away)

        home_event_counts['Blocked Shots'] = len(away[away['Detail 2'] == "Blocked"])
        away_event_counts['Blocked Shots'] = len(home[home['Detail 2'] == "Blocked"])


        home_event_counts['Shot Distance'] = home[(home['Event'] == "Shot") & (home['Detail 2'] == "On Net")]['Distance']
        away_event_counts['Shot Distance'] = away[(away['Event'] == "Shot") & (away['Detail 2'] == "On Net")]['Distance']

        home_event_counts['Goal Distance'] = home[home['Event'] == "Goal"]['Distance']
        away_event_counts['Goal Distance'] = away[away['Event'] == "Goal"]['Distance']

        if focused_team == ht:
            focused_event_counts = home_event_counts
            opposition_event_counts = away_event_counts
            teams['focused_team'] = ht
            teams['opposition_team'] = at

        if focused_team == at:
            focused_event_counts = away_event_counts
            opposition_event_counts = home_event_counts
            teams['focused_team'] = at
            teams['opposition_team'] = ht




        return focused_event_counts,opposition_event_counts,teams

    def get_shots_goals_single_game(self,game,focused_team):

        home,away = self._get_event_locations_single_game(['Goal','Shot'],game=game)
        ht = list(home['Home Team'])[0]
        at = list(away['Away Team'])[0]
        teams = {}


        home_all_locations = home[['X Coordinate', 'Y Coordinate']]
        away_all_locations = away[['X Coordinate', 'Y Coordinate']]


        home_shot_locations = home[(home['Event'] == 'Shot') & (home['Detail 2'] == "On Net")][['X Coordinate', 'Y Coordinate']]
        away_shot_locations = away[(away['Event'] == 'Shot') & (away['Detail 2'] == "On Net")][['X Coordinate', 'Y Coordinate']]

        home_goal_locations = home[home['Event'] == 'Goal'][['X Coordinate', 'Y Coordinate']]
        away_goal_locations = away[away['Event'] == 'Goal'][['X Coordinate', 'Y Coordinate']]

        home_events = [home_all_locations, home_shot_locations, home_goal_locations]
        away_events = [away_all_locations, away_shot_locations, away_goal_locations]

        if focused_team == ht:
            focused_events = home_events
            opposition_events = away_events
            teams['focused_team'] = ht
            teams['opposition_team'] = at

        if focused_team == at:
            focused_events = away_events
            opposition_events = home_events
            teams['focused_team'] = at
            teams['opposition_team'] = ht


        return focused_events, opposition_events, teams

    def check_overtime(self,game):
        is_overtime = 4 in self.df[self.df['game_date'] == game]['Period'].values
        return is_overtime

    def get_summary(self,focused_team,game,event):
        game_data = self.df[self.df['game_date'] == game]
        home, away = self._get_event_locations_single_game([event], game=game)
        OT = self.check_overtime(game)
        home_event_counts = {}
        away_event_counts = {}
        for period in [1,2,3,4]:
            home_event_counts[period] = len(home[home['Period'] == period])
            away_event_counts[period] = len(away[away['Period'] == period])
        home_event_counts['Total'] = len(home)
        away_event_counts['Total'] = len(away)

        ht = list(game_data['Home Team'])[0]
        at = list(game_data['Away Team'])[0]
        teams = {}

        if focused_team == ht:
            focused_event_counts = home_event_counts
            opposition_event_counts = away_event_counts
            teams['focused_team'] = ht
            teams['opposition_team'] = at

        if focused_team == at:
            focused_event_counts = away_event_counts
            opposition_event_counts = home_event_counts
            teams['focused_team'] = at
            teams['opposition_team'] = ht

        df = pd.DataFrame({'':[teams['focused_team'],teams['opposition_team']],
                           '1st':[focused_event_counts[1], opposition_event_counts[1]],
                           '2nd':[focused_event_counts[2], opposition_event_counts[2]],
                           '3rd':[focused_event_counts[3], opposition_event_counts[3]],
                           'OT':[focused_event_counts[4] if OT else "N/A", opposition_event_counts[4] if OT else "N/A"],
                           'Total':[focused_event_counts['Total'],opposition_event_counts['Total']]
                           })

        return df


