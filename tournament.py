#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

# delete data from the matches table
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()

#delete data from the players table
def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM players;")
    conn.commit()
    conn.close()

#count all rows from the players table and fetch the one result
def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM players;")
    result = cur.fetchone()
    return result[0]
    conn.close()

#insert the players name into the players table in the name column
def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

#find out number of wins and matches for each player. Left join players and matches tables where match_id
#is equal to player id. Group the results by player id and then order them by numWins in a descending order
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
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id, name, (SELECT COUNT(*) FROM matches '
                'WHERE winner_id = id) as numWins, (SELECT COUNT(*) '
                'FROM matches WHERE id IN (winner_id, loser_id)) as numMatches '
                'FROM players LEFT JOIN matches ON match_id = players.id '
                'GROUP BY players.id ORDER BY numWins DESC;')

    standings = cur.fetchall()
    conn.close()
    return standings

#insert into the matches table the winner and loser id in the respective columns
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO matches (winner_id, loser_id) "
                "VALUES (%s, %s)", (winner, loser,))
    conn.commit()
    conn.close()


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
    #Current standings
    standings = playerStandings()

    #number of total matches is half of number of elements in standings
    total_matches = len(standings)/2

    #next player
    p = 0

    #list of pairings
    pairings = []

    for i in range(total_matches):
        if i == 0:
            # match between top 2 players based on their standings
            pairings.append((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
        else:
            #matches subsequent players based on their standings
            pairings.append((standings[p][0], standings[p][1], standings[p+1][0], standings[p+1][1]))
        p += 2

    return pairings
