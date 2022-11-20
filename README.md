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
14 GP 31:55 MPG
23.5 pts 10.7 reb 2.3 ast
0.548 FG% (9.0 FG / 16.4 FGA)
0.235 3PT% (0.3 3PT / 1.2 3PTA)
0.802 FT% (5.2 FT / 6.5 FTA)
```

### `games`

```
usage: nba.py games [-h] [-d] [-n GAMES] [-o TEAM] [--lookback SEASONS] name [name ...]

Reports stats from the last 5 games for the given player.

positional arguments:
  name                Player name, specify first/last/both as needed

optional arguments:
  -h, --help          show this help message and exit
  -d, --debug         Enable debug output.
  -n GAMES            Number of games
  -o TEAM             Opponent
  --lookback SEASONS  Grab games from previous seasons
```

Examples:

```
$ nba.py games Lonnie Walker IV -n 8 -d
Lonnie Walker IV - G (LAL)
11/13 v. BKN: 25 pts 1 reb 0 ast
10/18 @  GSW: 5 pts 3 reb 5 ast
11/09 @  LAC: 0 pts 0 reb 0 ast
11/11 v. SAC: 19 pts 1 reb 1 ast
11/04 v. UTA: 17 pts 1 reb 1 ast
11/18 v. DET: 17 pts 1 reb 3 ast
11/02 v. NOP: 28 pts 3 reb 1 ast
11/07 @  UTA: 0 pts 0 reb 0 ast
```