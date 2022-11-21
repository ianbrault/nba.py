![version](https://img.shields.io/github/v/release/ianbrault/nba.py?display_name=tag) ![license](https://img.shields.io/github/license/ianbrault/nba.py)

# nba.py

Queries useful NBA statistics using the [balldontlie](https://www.balldontlie.io/) API.

## Commands

### `avg`

```
usage: nba.py avg [-h] [-d] name [name ...]

Reports season averages for the given player.

positional arguments:
  name         Player name, specify first/last/both as needed

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Enable debug output.
```

Examples:

```
$ nba.py avg Anthony Davis
Anthony Davis - F-C (LAL)
13 GP 34.4 MPG
25.3 pts 11.5 reb 2.5 ast
0.548 FG% (9.7 FG / 17.7 FGA)
0.235 3PT% (0.3 3PT / 1.3 3PTA)
0.802 FT% (5.6 FT / 7.0 FTA)
```

### `games`

```
usage: nba.py games [-h] [-d] [-n GAMES] [-o TEAM] [--lookback SEASONS] name [name ...]

Reports stats from the last 5 games for the given player.

positional arguments:
  name                Player name, specify first/last/both as needed

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Enable debug output.
  -n GAMES     Number of games
  -o TEAM      Opponent
  -l SEASONS   Lookback to grab games from previous seasons
```

Examples:

```
$ nba.py games Lonnie Walker IV -n 8 -d
Lonnie Walker IV - G (LAL)
11/13 v. BKN: 25 pts 1 reb 0 ast
10/18 @  GSW: 5 pts 3 reb 5 ast
11/11 v. SAC: 19 pts 1 reb 1 ast
11/04 v. UTA: 17 pts 1 reb 1 ast
11/18 v. DET: 17 pts 1 reb 3 ast
11/02 v. NOP: 28 pts 3 reb 1 ast
11/06 v. CLE: 6 pts 1 reb 1 ast
10/30 v. DEN: 18 pts 5 reb 2 ast
```

```
$ nba.py games Russell Westbrook -o BKN -l 2
Russell Westbrook - G (LAL)
11/13/2022 v. BKN: 14 pts 6 reb 12 ast
01/25/2022 @  BKN: 15 pts 6 reb 4 ast
12/25/2021 v. BKN: 13 pts 12 reb 11 ast
03/21/2021 @  BKN: 29 pts 13 reb 13 ast
01/03/2021 @  BKN: 24 pts 5 reb 10 ast
```