import sqlite3
import pandas as pd

def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_game_id_table(conn):
    cur = conn.cursor()

    drop_string = """DROP TABLE IF EXISTS game_id_table;"""
    cur.execute(drop_string)
    create_string = """CREATE TABLE IF NOT EXISTS game_id_table (
                                    GAME_ID integer PRIMARY KEY,
                                    SEASON_ID integer NOT NULL,
                                    GAME_DATE date NOT NULL,
                                    TEAM_ID_HOME integer NOT NULL,
                                    TEAM_ID_AWAY integer NOT NULL,
                                    TEAM_ABBREVIATION_HOME string NOT NULL,
                                    TEAM_ABBREVIATION_AWAY string NOT NULL
                                );"""


    cur.execute(create_string)
    cur.execute('SELECT GAME_ID,SEASON_ID, GAME_DATE, TEAM_ID_HOME, TEAM_ID_AWAY, TEAM_ABBREVIATION_HOME, TEAM_ABBREVIATION_AWAY from Game')

    rows = cur.fetchall()

    insert_string = """INSERT INTO game_id_table
                          (GAME_ID, SEASON_ID, GAME_DATE, TEAM_ID_HOME, TEAM_ID_AWAY, TEAM_ABBREVIATION_HOME, TEAM_ABBREVIATION_AWAY) 
                          VALUES (?, ?, ?, ?, ?, ?, ?);"""
    game_id_set = set()
    for row in rows:
        if row[0] in game_id_set:
            pass
        else:
            game_id_set.add(row[0])
            cur.execute(insert_string, row)
    conn.commit()
    cur.close()

def get_game_ids(conn):
    cur = conn.cursor()

    drop_string = """SELECT GAME_ID FROM game_id_table"""
    cur.execute(drop_string)
    rows = cur.fetchall()
    return rows


con = create_connection('../game_data/basketball.sqlite')

create_game_id_table(con)
print(get_game_ids(con))

# SELECT column_name, COUNT(*) FROM table_name GROUP BY column_name ORDER BY 2 DESC;
# Query = "SELECT ASSISTED, COUNT(*)  FROM GameInfo GROUP BY ASSISTED ORDER BY 2 DESC"
# dict = {}
# for row in con.execute(Query):
#     dict[row[0]] = row[1]
#
# print(dict[1]/(dict[1]+dict[0]))
