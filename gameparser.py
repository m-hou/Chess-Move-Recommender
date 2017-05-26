import pgn
import sqlite3

FILE_NAME = "ficsgamesdb_201701_standard2000_nomovetimes_1465638.pgn"
LARGE_FILE_NAME = "ficsgamesdb_201701_chess_nomovetimes_1465381.pgn"

for game in pgn.GameIterator(LARGE_FILE_NAME):
    conn = sqlite3.connect("games.sqlite")
    c = conn.cursor()
    g = (game.result, game.blackelo, game.whiteelo, game.timecontrol, ", ".join(game.moves[:-2]))
    c.execute("INSERT INTO Games VALUES (?,?,?,?,?)", g)
conn.commit()
conn.close()
