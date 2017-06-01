import sqlite3

DB = "games.sqlite"

def queryDB(query, *args):
    """doc"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(query, *args)
    count = c.fetchall()
    conn.close()
    return count

def winningMoves(moves):
    """doc"""
    return queryDB(
        """
        SELECT
            SUBSTR(Moves, ?, INSTR(SUBSTR(Moves, ?), ?)) AS nextmove,
            ROUND(
                SUM(
                    CASE WHEN Result = '1-0' THEN 1
                    WHEN Result = '1/2-1/2' THEN 0.5
                    WHEN Result = '0-1' THEN 0
                    ELSE 0
                    END
                ) / count(*),
                4
            ) AS winrate
        FROM Games
        WHERE
            Moves LIKE ?
        GROUP BY nextmove
        ORDER BY winrate DESC
        LIMIT 20
        """, (len(moves) + 3, len(moves) + 4, ",", moves + "%"))


def popularMoves(moves):
    """doc"""
    return queryDB(
        """
        SELECT
            SUBSTR(Moves, ?, INSTR(SUBSTR(Moves, ?), ?)) AS nextmove,
            count(*)
        FROM Games
        WHERE
            Moves LIKE ?
        GROUP BY nextmove
        ORDER BY count(*) DESC
        LIMIT 20
        """, (len(moves) + 3, len(moves) + 4, ",", moves + "%"))

moves = input('Enter moves: ')
print(*popularMoves(moves))
print(*winningMoves(moves))
