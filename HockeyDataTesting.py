import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
file1 = r"C:\Users\Alex\PycharmProjects\HockeyDataVisualization\olympic_womens_dataset.csv"
file2 = r"C:\Users\Alex\PycharmProjects\HockeyDataVisualization\hackathon_womens.csv"
rink_image = mpimg.imread(r"C:\Users\Alex\PycharmProjects\HockeyDataVisualization\rink_coords_cropped.png")
df = pd.read_csv(file1)
# df2 = pd.read_csv(file2)
# print(df.head)
game_days = df['game_date'].unique()
for gd in game_days:
    game_data = df[df['game_date'] == gd]
    assert len(game_data['Home Team'].unique()) == 1 #Maybe multiple games on one day?
    assert len(game_data['Away Team'].unique()) == 1  # Maybe multiple games on one day?
    home_team = list(game_data['Home Team'])[0]
    away_team = list(game_data['Away Team'])[0]

    home_team_events = game_data[game_data['Team'] == home_team]
    away_team_events = game_data[game_data['Team'] == away_team]


    #Set limits to coordinates for rink
    fig, ax = plt.subplots(1,1,sharex=True,sharey=True)
    ax.set_xlim(0,200)
    ax.set_ylim(0,85)
    ax.imshow(rink_image, aspect='auto', extent=(0, 200, 0, 85), zorder=-1)
    # plot shots:50
    home_shot_locations = home_team_events[home_team_events['Event'] == 'Shot'][['X Coordinate','Y Coordinate']]
    away_shot_locations = away_team_events[away_team_events['Event'] == 'Shot'][['X Coordinate','Y Coordinate']]

    home_goal_locations = home_team_events[home_team_events['Event'] == 'Goal'][['X Coordinate','Y Coordinate']]
    away_goal_locations = away_team_events[away_team_events['Event'] == 'Goal'][['X Coordinate','Y Coordinate']]
    cmap_home = sns.cubehelix_palette(start=2, light=1, as_cmap=True)
    cmap_away = sns.cubehelix_palette(start=0, light=1, as_cmap=True)

    #home heatmap
    sns.kdeplot(
        x=home_shot_locations['X Coordinate'], y=home_shot_locations['Y Coordinate'],
        cmap=cmap_home, fill=True,clip=((100, 200),(0,85)),
        thresh=0, levels=10,
        ax=ax,alpha=0.5
    )
    #away heatmap
    sns.kdeplot(
        x=200-away_shot_locations['X Coordinate'], y=away_shot_locations['Y Coordinate'],
        cmap=cmap_away, fill=True,clip=((0, 100),(0,85)),
        thresh=0, levels=10,
        ax=ax,alpha=0.5
    )

    # sns.kdeplot(x=home_shot_locations['X Coordinate'], y=home_shot_locations['Y Coordinate'])
    ax.scatter(home_shot_locations['X Coordinate'],home_shot_locations['Y Coordinate'],marker='x',color='b',label=home_team)
    ax.scatter(home_goal_locations['X Coordinate'], home_goal_locations['Y Coordinate'], marker='o', color='gold',edgecolor='b')
    ax.scatter(200-away_shot_locations['X Coordinate'], away_shot_locations['Y Coordinate'], marker='x',color='r',label=away_team)
    ax.scatter(200-away_goal_locations['X Coordinate'], away_goal_locations['Y Coordinate'], marker='o', color='gold',edgecolor='r')
    # ax.hist2d(home_shot_locations['X Coordinate'],home_shot_locations['Y Coordinate'],bins=[20,9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=2)

    fig.set_size_inches(15, 6.375)
    plt.show()
