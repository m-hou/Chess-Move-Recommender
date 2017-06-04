# Chess Move Recommender

This repository contains the backend prototype for a chess move recommender browser extension that aggregates data about next possible moves given a list of previously played moves.


### Overview

gameparser.py parses a pgn file and imports the data into a SQLite file. gameaggregator.py takes a SQLite file and queries it for different statistics. Currently, it can show the most popular moves and the highest win rate moves.


### Usage

Step 1:
Find a pgn file online from a game database. I used [FICS Games Database]( http://ficsgames.org/cgi-bin/download.cgi).

Step 2:
Create a sqlite file with a table named 'Games' and the rows 'Result', 'BlackElo', 'WhiteElo', 'TimeControl', 'Moves'.
Create statement:
```
CREATE TABLE `Games` ( `Result` TEXT NOT NULL, `BlackElo` INTEGER NOT NULL, `WhiteElo` INTEGER NOT NULL, `TimeControl` TEXT NOT NULL, `Moves` TEXT NOT NULL )
```

Step 3:
Run gameparser.py to populate the SQLite database.

Step 4:
Run gameaggregator.py to get statistics.

*Note: gameaggrator.py will ask for a move input, enter moves as comma seperated values.

Here's what you can expect:
```
$ python gameaggregator.py games.sqlite
Enter moves: e4, e5, Nf3
popularMoves took 29.160880s to execute.
('Nc6', 830161) ('d6', 321124) ('Nf6', 133265) ('Bc5', 34465) ('d5', 32538) ('f5', 25298) ('Qf6', 19188) ('f6', 6870) ('Bd6', 6828) ('Qe7', 4619) ('', 2768) ('c6', 2311) ('b6', 989) ('c5', 682) ('g6', 656) ('h6', 622) ('a6', 566) ('Bb4', 383) ('Be7', 301) ('Ne7', 168)
winningMoves took 31.386538s to execute.
('f5', 0.5327) ('d5', 0.4941) ('Nf6', 0.4929) ('Nc6', 0.4737) ('', 0.4669) ('Qe7', 0.4394) ('d6', 0.4362) ('Qf6', 0.4352) ('Bc5', 0.4266) ('Bd6', 0.414) ('c6', 0.3992) ('c5', 0.3717) ('b5', 0.371) ('Be7', 0.3405) ('b6', 0.3367) ('g6', 0.3361) ('h6', 0.3352) ('a6', 0.3339) ('f6', 0.2779) ('a5', 0.2761)
```
Output can be read as:
popularMoves: (move, frequency of move)
winningMoves: (move, winrate)


### Next Steps

Currently, I am working on a Chrome extension take observes DOM changes on a chess website to get the moves and pass it to my backend, which will be this prototype as a Flask/Django app. The extension will render the data on the side of the page and provide real-time data visualization for next possible moves.

Some other challenges include back-end performance. I have timed function calls set up on gameaggregator.py
and so far I am getting:

On 955k rows:
~4s/query with the move input ""
~1s/query with the move input "e4, e5"

On 12.4m rows:
~120s/query with the move input ""
~40s/query with the move input "e4, e5"

As you can tell, these response times are sub-optimal. I am currently investigating some different solutions
such as indexing and other SQL optimizations; however, NoSQL (MongoDB) or GraphDBs (Neo4j) may be the way to go.


### Contributors

My friend [Austin](https://github.com/ahendy) for playing chess with me and inspiring me to start this project along with encouraging me to try out Python.

[Renatopp's PGNParser](https://github.com/renatopp/pgnparser), which I am using to help parse PGN files. The parser is written in Python 2.7, so I updated it (in my repo as pgn.py) to work for 3.6.
