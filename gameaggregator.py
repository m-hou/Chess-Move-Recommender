import sqlite3

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
