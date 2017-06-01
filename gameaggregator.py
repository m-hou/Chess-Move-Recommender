import sqlite3

def winningMoves(moves):
    """doc"""
    conn = sqlite3.connect("games.sqlite")
    c = conn.cursor()
    c.execute("""SELECT SUBSTR(Moves, ?, INSTR(SUBSTR(Moves, ?), ?)) AS nextmove,
                 ROUND(
                    SUM(
                        CASE WHEN Result = '1-0' THEN 1
                        WHEN Result = '1/2-1/2' THEN 0.5
                        WHEN Result = '0-1' THEN 0
                        ELSE 0
                        END
                    ) / count(*),
                 4) as winrate
                 FROM Games
                 WHERE Moves
                 LIKE ?
                 GROUP BY nextmove
                 ORDER BY winrate DESC
                 LIMIT 20""", (len(moves) + 3, len(moves) + 4, ",", moves + "%"))
    count = c.fetchall()
    conn.close()
    return count

def popularMoves(moves):
    """doc"""
    conn = sqlite3.connect("games.sqlite")
    c = conn.cursor()
    c.execute("""SELECT SUBSTR(Moves, ?, INSTR(SUBSTR(Moves, ?), ?)) AS nextmove, count(*)
                 FROM Games
                 WHERE Moves
                 LIKE ?
                 GROUP BY nextmove
                 ORDER BY count(*) DESC
                 LIMIT 20""", (len(moves) + 3, len(moves) + 4, ",", moves + "%"))
    count = c.fetchall()
    conn.close()
    return count

moves = input('Enter moves: ')
print(*popularMoves(moves))
print(*winningMoves(moves))
