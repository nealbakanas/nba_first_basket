from enum import Enum



class EventMsgType(Enum):
    FIELD_GOAL_MADE = 1
    FIELD_GOAL_MISSED = 2
    FREE_THROWfree_throw_attempt = 3
    REBOUND = 4
    TURNOVER = 5
    FOUL = 6
    VIOLATION = 7
    SUBSTITUTION = 8
    TIMEOUT = 9
    JUMP_BALL = 10
    EJECTION = 11
    PERIOD_BEGIN = 12
    PERIOD_END = 13


def jump_ball_helper(first_play):
    if first_play['PLAYER1_TEAM_ABBREVIATION'] == first_play['PLAYER3_TEAM_ABBREVIATION']:
        return {"TIP_WINNER_NAME": first_play['PLAYER1_NAME'],
                "TIP_WINNER_PLAYER_ID": first_play['PLAYER1_ID'],
                "TIP_WINNER_TEAM_ID": first_play['PLAYER1_TEAM_ID'],
                "TIP_WINNER_TEAM_ABBREVIATION": first_play["PLAYER1_TEAM_ABBREVIATION"],
                "TIP_LOSER_NAME": first_play['PLAYER2_NAME'],
                "TIP_LOSER_PLAYER_ID": first_play['PLAYER2_ID']}
    else:
        return {"TIP_WINNER_NAME": first_play['PLAYER2_NAME'],
                "TIP_WINNER_PLAYER_ID": first_play['PLAYER2_ID'],
                "TIP_WINNER_TEAM_ID": first_play['PLAYER2_TEAM_ID'],
                "TIP_WINNER_TEAM_ABBREVIATION": first_play["PLAYER2_TEAM_ABBREVIATION"],
                "TIP_LOSER_NAME": first_play['PLAYER1_NAME'],
                "TIP_LOSER_PLAYER_ID": first_play['PLAYER1_ID']}


from nba_api.stats.endpoints import playbyplayv2
import time
import pandas as pd
import csv

game_ids = pd.read_csv("../Files/Archive/GameIDs2016-2020.csv", dtype=str)
# game_ids = ['0021700786', '0021400506', '0021400491', '0021600735', '0021200947']
game_ids['PULLED'] = False

skipped_games = []

column_names = ['GAME_ID', 'TIP_WINNER_NAME', 'TIP_WINNER_PLAYER_ID', 'TIP_WINNER_TEAM_ID',
                'TIP_WINNER_TEAM_ABBREVIATION', 'TIP_LOSER_NAME', "TIP_LOSER_PLAYER_ID",
                'FIRST_BASKET_PLAYER_NAME', 'FIRST_BASKET_PLAYER_ID',
                'FIRST_BASKET_PLAYER_TEAM_ID', 'FIRST_BASKET_PLAYER_TEAM_ABBR',
                'TIP_AND_FIRST_BASKET']

final_df = pd.DataFrame(columns=column_names)

seen_games = set()
for i, row in game_ids.iterrows():



    game = playbyplayv2.PlayByPlayV2(game_id=row['GAME_ID'])
    print(game.get_normalized_dict()['PlayByPlay'][1:])

    print(row['GAME_ID'])

    if row['GAME_ID'] in seen_games:
        continue
    else:

        time.sleep(3)
        quit()
        try:
            jump_ball = jump_ball_helper(game.get_normalized_dict()['PlayByPlay'][1])
            row['PULLED'] = True
            for play in game.get_normalized_dict()['PlayByPlay'][1:]:
                if play['EVENTMSGTYPE'] == 1:
                    print(play)
                    if play['PLAYER2_ID'] == 0:
                        assisted = False
                    else:
                        assisted = True
                    first_basket_info = {"GAME_ID": play['GAME_ID'],
                                         "FIRST_BASKET_PLAYER_NAME": play['PLAYER1_NAME'],
                                         "FIRST_BASKET_PLAYER_ID": play['PLAYER1_ID'],
                                         "FIRST_BASKET_PLAYER_TEAM_ID": play['PLAYER1_TEAM_ID'],
                                         "FIRST_BASKET_PLAYER_TEAM_ABBR": play['PLAYER1_TEAM_ABBREVIATION'],
                                         "ASSISTED": assisted}
                    break

            game_ids.at[i,'PULLED'] = True

        except IndexError:
            skipped_games.append(row['GAME_ID'])
            game_ids.at[i,'PULLED'] = True
            continue
        seen_games.add(row['GAME_ID'])

        # print(jump_ball)
    final_dict = {**jump_ball, **first_basket_info}
    if final_dict['TIP_WINNER_TEAM_ID'] == final_dict["FIRST_BASKET_PLAYER_TEAM_ID"]:
        final_dict['TIP_AND_FIRST_BASKET'] = 1
    else:
        final_dict['TIP_AND_FIRST_BASKET'] = 0

    final_df = final_df.append(final_dict, ignore_index=True)
    final_df.to_csv('../Files/TempGameInfo.csv', index=False)
    game_ids.to_csv('../Files/TrackerGameIDs.csv', index = False)

final_df.to_csv('../Files/AllGameInfo2016-2020.csv', index=False)

skipped_file = open("Skipped_GameIDs.txt", "w")
skipped_file.write(skipped_games)
