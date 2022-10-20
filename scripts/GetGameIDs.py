from nba_api.stats.static import *
from nba_api.stats.library.parameters import *
from nba_api.stats.endpoints import leaguegamefinder
import re
import csv
import time
import pandas as pd

nba_teams = teams.get_teams()
team_ids = [(team['full_name'], team['id']) for team in nba_teams]

# test = [team for team in nba_teams if team['full_name'] in ['Oklahoma City Thunder','New York Knicks']]

end_year = 22015


column_names = ['SEASON_ID','TEAM_ID','TEAM_ABBREVIATION','GAME_ID','GAME_DATE','PULLED']

final_df = pd.DataFrame(columns = column_names)


for team in team_ids:
    # print(team[0])
    print(team)
    time.sleep(15)
    game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team[1],
                                                    season_type_nullable=SeasonTypeRegularPlayoffs().regular)
    games = game_finder.get_data_frames()[0]

    games['SEASON_ID'] = pd.to_numeric(games['SEASON_ID'])
    # for year in years:
    target_games = games[games['SEASON_ID'] > end_year]

    target_data = target_games[['SEASON_ID','TEAM_ID','TEAM_ABBREVIATION','GAME_ID','GAME_DATE']]

    final_df = pd.concat([final_df,target_data])

final_df.to_csv('../Files/GameIDs2016-2020.csv',index=False)

