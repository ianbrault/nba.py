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
  -b           Log only a basic points/rebounds/assists slashline
  -n GAMES     Number of games
  -o TEAM      Opponent
  -l SEASONS   Lookback to grab games from previous seasons
```

Examples:

```
$ nba.py games Lonnie Walker IV -n 8
Lonnie Walker IV - G (LAL)
11/13/2022 v.BKN  25 pts  1 reb  0 ast  9-15 FG  4-5 3PT  3-3 FT
10/18/2022 @ GSW   5 pts  3 reb  5 ast   2-7 FG  0-3 3PT  1-2 FT
11/11/2022 v.SAC  19 pts  1 reb  1 ast  8-14 FG  2-4 3PT  1-2 FT
11/04/2022 v.UTA  17 pts  1 reb  1 ast  6-12 FG  2-3 3PT  3-3 FT
11/18/2022 v.DET  17 pts  1 reb  3 ast  6-13 FG  1-4 3PT  4-4 FT
11/02/2022 v.NOP  28 pts  3 reb  1 ast  9-17 FG  5-9 3PT  5-6 FT
11/06/2022 v.CLE   6 pts  1 reb  1 ast   3-7 FG  0-3 3PT  0-0 FT
10/30/2022 v.DEN  18 pts  5 reb  2 ast  6-14 FG  3-5 3PT  3-4 FT
```

```
$ nba.py games Russell Westbrook -o BKN -l 2 -b
Russell Westbrook - G (LAL)
11/13/2022 v.BKN  14 pts   6 reb  12 ast
01/25/2022 @ BKN  15 pts   6 reb   4 ast
12/25/2021 v.BKN  13 pts  12 reb  11 ast
03/21/2021 @ BKN  29 pts  13 reb  13 ast
01/03/2021 @ BKN  24 pts   5 reb  10 ast
```