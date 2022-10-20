import sqlite3
import pandas as pd

con = sqlite3.connect("../Master.db")
Warriors_Blazers = ["Stephen Curry",
                    "Andrew Wiggins",
                    "Kelly Oubre Jr.",
                    "Kevon Looney",
                    "Draymond Green",
                    "Damian Lillard",
                    "Enes Kanter",
                    "Gary Trent Jr.",
                    "Robert Covington",
                    "Derrick Jones Jr."]

Jazz_Sixers = ["Joel Embiid",
               "Rudy Gobert",
               "Donovan Mitchell",
               "Tobias Harris",
               "Bojan Bogdanovic",
               "Mike Conley",
               "Ben Simmons",
               "Seth Curry",
               "Danny Green",
               "Royce O'Neale"]

Pacers_Cavs = ["Malcolm Brogdon",
               "Jarrett Allen",
               "Collin Sexton",
               "Domantas Sabonis",
               "Darius Garland",
               "Doug McDermott",
               "Myles Turner",
               "Justin Holiday",
               "Isaac Okoro",
               "Dean Wade"]

Nets_Rockets = ["Kyrie Irving", "James Harden", "Victor Oladipo", "John Wall", "Joe Harris", "DeAndre Jordan",
                "Danuel House Jr.", "P.J. Tucker", "Justin Patton", "Bruce Brown"]

Bulls_Pelicans = ["Zach LaVine", "Brandon Ingram", "Zion Williamson", "Coby White", "Steven Adams", "Eric Bledsoe",
                  "Wendell Carter Jr.", "Lonzo Ball", "Patrick Williams", "Garrett Temple"]

Hornets_Twolves = ["Karl-Anthony Towns", "Terry Rozier", "LaMelo Ball", "Anthony Edwards", "Josh Okogie", "Ricky Rubio",
                   "Jarred Vanderbilt", "P.J. Washington", "Bismack Biyombo", "Cody Martin"]

Hawks_Sixers = ['Joel Embiid','Trae Young','Ben Simmons','Tobias Harris','Bogdan Bogdanovic','Clint Capela','John Collins','Seth Curry','Danny Green','Solomon Hill']

# Thunder_Mavericks = []

# Lakers_Kings = []
# #
FirstBasketQuery = "SELECT FIRST_BASKET_PLAYER_NAME,FIRST_" \
                   "BASKET_PLAYER_ID, " \
                   "COUNT(*) AS TOTAL FROM GameInfo " \
                   "GROUP BY FIRST_BASKET_PLAYER_ID " \
                   "ORDER BY TOTAL DESC"
for row in con.execute(FirstBasketQuery):
    if row[0] in Hawks_Sixers:
        print(row)

embiid_jokic = ["Joel Embiid","Clint Capela"]
TipOffQuery = "SELECT DISTINCT(GameInfo.TIP_WINNER_NAME) AS PLAYER, TipOffElo.PLAYER_ID AS PLAYER_ID, TipOffElo.RATING AS RATING FROM GameInfo,TipOffElo WHERE GameInfo.TIP_WINNER_PLAYER_ID = TipOffElo.PLAYER_ID"
for row in con.execute(TipOffQuery):
    if row[0] in embiid_jokic:
        print(row)

# SELECT column_name, COUNT(*) FROM table_name GROUP BY column_name ORDER BY 2 DESC;
# Query = "SELECT ASSISTED, COUNT(*)  FROM GameInfo GROUP BY ASSISTED ORDER BY 2 DESC"
# dict = {}
# for row in con.execute(Query):
#     dict[row[0]] = row[1]
#
# print(dict[1]/(dict[1]+dict[0]))
