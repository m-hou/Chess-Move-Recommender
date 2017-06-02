import sqlite3
import time
from functools import update_wrapper

DB = "games.sqlite"

def decorator(d):
    """doc"""
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

decorator = decorator(decorator)

@decorator
def timedcall(f):
    def timedcall_f(*arg, **kw):
        """doc"""
        start = time.time()
        res = f(*arg, **kw)
        end = time.time()
        print("%s took %fs to execute." % (f.__name__, end - start))
        return res
    return timedcall_f

def queryDB(query, *args):
    """doc"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(query, *args)
    count = c.fetchall()
    conn.close()
    return count

@timedcall
def winningMoves(moves):
    """doc"""
    return queryDB(
        """
        SELECT
            SUBSTR(Moves, ?, INSTR(SUBSTR(Moves, ?), ?)) AS nextmove,
            ROUND(
                SUM(
                    CASE WHEN Result = '1-0' THEN ?
                    WHEN Result = '1/2-1/2' THEN 0.5
                    WHEN Result = '0-1' THEN ?
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
        """, (len(moves) + 3, len(moves) + 4, ",", (len(moves) + 1) % 2, len(moves) % 2 , moves + "%"))

@timedcall
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
