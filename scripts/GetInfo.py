import requests
import pandas as pd
import numpy as np
import io
from nba_api.stats.static import teams
import time
from nba_api.stats.endpoints import leaguegamefinder
import matplotlib.pyplot as plt
# from joypy import joyplot

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

play_by_play_url = "https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_0042000404.json"
response = requests.get(url=play_by_play_url, headers=headers).json()
play_by_play = response['game']['actions']
df = pd.DataFrame(play_by_play)

# get game logs from the reg season
gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable='2020-21',
                                              league_id_nullable='00',
                                              season_type_nullable='Regular Season')
games = gamefinder.get_data_frames()[0]
# Get a list of distinct game ids
game_ids = games['GAME_ID'].unique().tolist()
# create function that gets pbp logs from the 2020-21 season
def get_play_by_play(game_id):
    play_by_play_url = "https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_"+game_id+".json"
    response = requests.get(url=play_by_play_url, headers=headers).json()
    play_by_play = response['game']['actions']
    df = pd.DataFrame(play_by_play)
    df['gameid'] = game_id
    return df

def get_tip_off(pbp):
    tip_off_participants = pbp[pbp['jumpBallWonPersonId'].notnull()]
    return tip_off_participants

# get data from all ids (takes awhile)
pbpdata = []
cnt = 0
for game_id in game_ids:
    cnt+=1
    print(game_id)
    game_data = get_play_by_play(game_id)
    tip_offs = get_tip_off(game_data)
    pbpdata.append(tip_offs)
    if cnt == 5:
        break
df = pd.concat(pbpdata, ignore_index=True)

# calculate time elapsed between a free throw and whatever action came before it
df = df.sort_values(by=['gameid', 'orderNumber'])
df.to_csv('test.csv')

###
# read in cleaned data from GitHub, if you want