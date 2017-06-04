import pgn
import sqlite3
import sys, getopt

def addGamesToDB(inputfile, outputfile, clear=False):
    """doc"""
    conn = sqlite3.connect(outputfile)
    c = conn.cursor()
    if clear:
        c.execute("DELETE FROM Games")
    gamesParsed = 0
    for index, game in enumerate(pgn.GameIterator(inputfile)):
        g = (game.result, game.blackelo, game.whiteelo, game.timecontrol, ", " + ", ".join(game.moves[:-2]))
        c.execute("INSERT INTO Games VALUES (?,?,?,?,?)", g)
        gamesParsed = index + 1
        if gamesParsed % 1000 == 0:
            print(gamesParsed)
    print(str(gamesParsed) + " games parsed")
    conn.commit()
    conn.close()

def main():
    exceptedFormat = "gameparser.py -i <inputfile.pgn> -o <outputfile.sqlite> [--clear]"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input=", "output=", "clear"])
    except getopt.GetoptError as err:
        print(err)
        print(exceptedFormat)
        sys.exit(2)

    clear = False
    inputFile = None
    outputFile = None
    for opt, arg in opts:
        if opt == "--clear":
            clear = True
        elif opt in ("-i", "--input"):
            inputFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
        else:
            assert False, "unhandled option"
    try:
        addGamesToDB(inputFile, outputFile, clear)
    except FileNotFoundError:
        print("file not found")
    except IOError:
        print(exceptedFormat)
        sys.exit(2)

if __name__ == "__main__":
    main()
