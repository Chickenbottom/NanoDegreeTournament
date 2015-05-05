#!/usr/bin/env python
# 
# Author: Chad Hickenbottom
# Nano Degree: Full Stack Web Developer
# About: Tournament.py Version 1.0
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("TRUNCATE game")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("truncate player, record, game;")
    DB.commit()    
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM player;")
    num = c.fetchone()
    DB.close()
    return num[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    print name
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO player (player_id, player_name) VALUES(DEFAULT, %s)", (bleach.clean(name),))
    c.execute("INSERT INTO tournament (tournament_id, name, location, tournament_begin_date, tournament_end_date) SELECT 1, 'first tourny', 'Seattle','1-1-2010', '1-5-2010' WHERE NOT EXISTS (SELECT tournament_id from tournament where tournament_id = 1);")
    c.execute("INSERT INTO record VALUES( (SELECT currval('player_player_id_seq')), 1, 0,0,0);")
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT player.player_id, player.player_name, record.wins, (select count(*) from game where game.player_1 = player.player_id or game.player_2 = player.player_id) as
     \"Games Played\" FROM player, record where (record.player_id = player.player_id)  group by player.player_id, record.wins;""")
    mtup = [(row[0], str(row[1]), row[2], row[3]) for row in c.fetchall()]
    DB.close()
    return mtup

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""INSERT INTO game (player_1, player_2, tournament_id, game_winner, game_loser) 
        VALUES ( (SELECT player_id FROM player WHERE player_id = %s), (SELECT player_id FROM player WHERE player_id = %s), 1, %s, %s)""", (bleach.clean(winner), bleach.clean(loser),bleach.clean(winner), bleach.clean(loser),))
    c.execute(" UPDATE record set wins = 1 where player_id = %s ", (bleach.clean(winner),))
    c.execute(" UPDATE record set loses = 1 where player_id = %s", (bleach.clean(loser),))
    DB.commit()
    DB.close()

 
    
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT player.player_id, player.player_name, record.wins, record.loses, record.draws FROM player, record where player.player_id = record.player_id order by record.wins, record.loses, record.draws")
    mtup = c.fetchall()
    DB.close()
    
    matches = []
    for tup in mtup:
        matches.append(tup[0])
        matches.append(tup[1])

    return zip(matches[0::4], matches[1::4], matches[2::4], matches[3::4])
