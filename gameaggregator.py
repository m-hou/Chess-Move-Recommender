import sqlite3
import sys, getopt
import tools

DB = "games.sqlite"

def queryDB(query, readFile, *args):
    """doc"""
    conn = sqlite3.connect(readFile)
    c = conn.cursor()
    c.execute(query, *args)
    count = c.fetchall()
    conn.close()
    return count

@tools.timedcall
def winningMoves(moves, readFile):
    """doc"""
    moveCount = len(moves.split(", ")) - 1
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
        """,
        readFile,
        (len(moves) + 3, len(moves) + 4, ",", (moveCount + 1) % 2, moveCount % 2, moves + "%"))

@tools.timedcall
def popularMoves(moves, readFile):
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
        """,
        readFile,
        (len(moves) + 3, len(moves) + 4, ",", moves + "%"))

def main():
    exceptedFormat = "gameaggregator.py <readfile.sqlite>"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "")
    except getopt.GetoptError as err:
        print(err)
        print(exceptedFormat)
        sys.exit(2)
    readFile = args[0]
    try:
        moves = input('Enter moves: ')
        if moves != "":
            moves = ", " + moves
        print(*popularMoves(moves, readFile))
        print(*winningMoves(moves, readFile))
    except FileNotFoundError:
        print("file not found")

if __name__ == "__main__":
    main()


