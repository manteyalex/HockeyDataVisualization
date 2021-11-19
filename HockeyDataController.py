from PyQt5.QtCore import QObject, pyqtSlot
import pandas as pd
class HockeyDataController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def get_games(self,team):
        games = self.model.get_team_games(team)
        return games

    def get_summary(self,team,games,event="Goal"):
        summary_total = None
        for game in games:
            summary = self.model.get_summary(team,game,event=event)
            if summary_total is None:
                summary_total = summary
                if len(games) > 1:
                    summary_total.iloc[1,0] = "Opposition"
                    summary_total = summary_total.replace('N/A',0)
            else:
                summary.iloc[1,0] = "Opposition"
                summary = summary.replace('N/A', 0)
                summary_total.iloc[:,1:] = summary_total.iloc[:,1:].add(summary.iloc[:,1:])

        return summary_total

    def get_shots_goals(self,team,games):
        focused_team, opposition_team, teams = None, None, None
        for game in games:
            if focused_team is None:
                focused_team, opposition_team, teams = self.model.get_shots_goals_single_game(game, team)
            else:
                new_focused, new_opposition, _ = self.model.get_shots_goals_single_game(game, team)
                for i in range(3):
                    focused_team[i] = focused_team[i].append(new_focused[i])
                    opposition_team[i] = opposition_team[i].append(new_opposition[i])
                teams['opposition_team'] = "Opposition"

        return focused_team, opposition_team, teams

    def get_detailed_shot_information(self,team,games):
        shot_attempts_focused, shot_attempts_opposition = 0, 0
        blocked_shots_focused, blocked_shots_opposition = 0, 0
        shot_distance_focused, shot_distance_opposition = None, None
        goal_distance_focused, goal_distance_opposition = None, None
        for game in games:
            focused_team, opposition_team, teams = self.model.get_detailed_shot_information(team, game)
            shot_attempts_focused += focused_team['Shot Attempts']
            shot_attempts_opposition += opposition_team['Shot Attempts']
            blocked_shots_focused += focused_team['Blocked Shots']
            blocked_shots_opposition += opposition_team['Blocked Shots']
            if shot_distance_focused is None:
                shot_distance_focused, shot_distance_opposition = focused_team['Shot Distance'], opposition_team['Shot Distance']
                goal_distance_focused, goal_distance_opposition = focused_team['Goal Distance'], opposition_team['Goal Distance']
            else:
                shot_distance_focused = shot_distance_focused.append(focused_team['Shot Distance'])
                shot_distance_opposition = shot_distance_opposition.append(opposition_team['Shot Distance'])

                goal_distance_focused = goal_distance_focused.append(focused_team['Goal Distance'])
                goal_distance_opposition = goal_distance_opposition.append(opposition_team['Goal Distance'])


            continue

        df = pd.DataFrame({'': ['Goals', 'Total Shots', 'SH%', 'Shot Attempts', 'Blocked Shots',
                                'Average Shot Distance (ft)', 'Average Goal Distance (ft)'],
                           teams['focused_team']: [0, 0, 0, shot_attempts_focused, blocked_shots_focused, shot_distance_focused.mean(), goal_distance_focused.mean()],
                           teams['opposition_team']: [0, 0, 0, shot_attempts_opposition, blocked_shots_opposition, shot_distance_opposition.mean(), goal_distance_opposition.mean()],

                           })

        return df, shot_distance_focused, shot_distance_opposition, goal_distance_focused, goal_distance_opposition