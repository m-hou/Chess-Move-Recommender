import sqlite3

def queryDB(moves):
    """doc"""
    conn = sqlite3.connect("games.sqlite")
    c = conn.cursor()
    c.execute("SELECT count(*) FROM Games WHERE Moves LIKE ?", (moves,))
    count = c.fetchone()
    conn.close()
    return count

moves = input('Enter moves: ')
print(*queryDB(moves))
