class EloSystem:

    def __init__(self,base = 1500,k = 20, k_prove = 40,prove_games = 20):
        # self.player_list = {}
        self.start_elo = base
        self.k = k
        self.k_prove = k_prove
        self.prove_games = prove_games
        self.players = []
        # self.elo_width = 400

    def get_player(self,name):

        for player in self.players:
            if player.name == name:
                return player
        else:
            return None

    # def contains(self, name):
    #     if


    def add_player(self,player,rating=None):
        if rating == None:
            rating = self.start_elo

        self.players.append(Player(name=player,rating=rating))

    # def remove_player

    def get_player_rating(self,name):
        return self.get_player(name).rating


    def record_match(self,name1,name2,winner=None,draw=False):

        player1 = self.get_player(name1)
        player2 = self.get_player(name2)

        expected1 = player1.compare_rating(player2)
        expected2 = player2.compare_rating(player1)

        rating1 = player1.rating
        rating2 = player2.rating

        if draw:
            score1 = 0.5
            score2 = 0.5
        elif winner == name1:
            score1 = 1.0
            score2 = 0.0
        elif winner == name2:
            score1 = 0.0
            score2 = 1.0
        else:
            raise IOError("Someone has to win here or at least draw dude")


        if player1.game_count <= self.prove_games:
            k_factor_1 = self.k_prove
        else:
            k_factor_1 = self.k

        if player2.game_count <= self.prove_games:
            k_factor_2 = self.k_prove
        else:
            k_factor_2 = self.k

        newRating1 = rating1 + k_factor_1 * (score1 - expected1)
        newRating2 = rating2 + k_factor_2 * (score2 - expected2)

        if newRating1 < 0:
            newRating1 = 0
            newRating2 = rating2 - rating1

        elif newRating2 < 0:
            newRating2 = 0
            newRating1 = rating1 - rating2

        player1.rating = newRating1
        player2.rating = newRating2

        player1.game_count += 1
        player2.game_count += 1

    def get_rating_list(self):

        l = []
        for player in self.players:
            l.append((player.name,player.rating))
        return l

class Player:

    def __init__(self,name,rating):
        self.name = name
        self.rating = rating
        self.game_count = 0

    def compare_rating(self,opponent):

        return (1 + 10 ** ((opponent.rating - self.rating)/400) ) ** -1


import pandas as pd
import sqlite3

con = sqlite3.connect("../Master.db")

cur = con.cursor()

df = pd.read_sql_query('SELECT GAME_ID,'
                       'TIP_WINNER_NAME,'
                       'TIP_WINNER_PLAYER_ID,'
                       'TIP_LOSER_NAME,TIP_LOSER_PLAYER_ID FROM GameInfo',con)


df = df.iloc[1:].fillna("FAKE PLAYER")

# print(TipOffHead)

Rankings = EloSystem()


for index,row in df.iterrows():
    winner = row['TIP_WINNER_PLAYER_ID']
    loser = row['TIP_LOSER_PLAYER_ID']
    if winner != "FAKE PLAYER" and loser != "FAKE PLAYER":
        if not Rankings.get_player(winner):
            Rankings.add_player(winner)
        if not Rankings.get_player(loser):
            Rankings.add_player(loser)
        # print(winner,loser)

        Rankings.record_match(winner,loser,winner)

new_df = pd.DataFrame(Rankings.get_rating_list(),columns=["PLAYER_ID","RATING"])
new_df.set_index('PLAYER_ID',inplace=True)
# new_df.to_sql("TipOffElo",con)

for row in con.execute('SELECT * FROM TipOffElo ORDER BY RATING DESC'):
    print(row)
# new_df.to_csv("../Files/Elo_Rankings.csv")
con.close()

