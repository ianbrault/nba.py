# Copyright (C) 2022  Ian Brault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from . import log
from . import state
from . import utils

from . import Game
from . import Player
from . import ScheduleGame

import bs4


def parse_players_stats_page(content):
    """
    Parses the per-game statistics for all players from the web page.

    Arguments:
        content : HTML content string

    Returns:
        a list of parsed Player objects
    """
    players = []
    soup = bs4.BeautifulSoup(content, "html.parser")
    # leave the following fields as strings, the remaining fields are assumed
    # to be floats
    str_fields = ["player", "pos", "team_id"]
    # the following fields have values wrapped inside links
    link_fields = ["player", "team_id"]

    table = soup.find("table", id="per_game_stats")
    for row in table.find_all("tr", class_="full_table"):
        player_info = {}
        for col in row.find_all("td"):
            key = col["data-stat"]
            if key in link_fields:
                value = col.a.string
            else:
                value = col.string
            if key not in str_fields:
                value = 0.0 if value is None else float(value)
            player_info[key] = value
        players.append(Player(**player_info))

    log.debug("parsed info for %u players" % len(players))
    return players


def parse_schedule_page(content):
    """
    Parses the season per-month game information from the web page.

    Arguments:
        content : HTML content string

    Returns:
        a list of parsed ScheduleGame objects
    """
    games = []
    soup = bs4.BeautifulSoup(content, "html.parser")
    # the following fields have values wrapped inside links
    link_fields = ["date_game", "visitor_team_name", "home_team_name"]
    # the following fields should be converted to ints
    int_fields = ["visitor_pts", "home_pts"]

    table = soup.find("table", id="schedule")
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if not cols or ("class" in row and row["class"] == "thead"):
            continue
        game_info = {}
        # date is in a th, remaining data is in td's
        game_info[row.th["data-stat"]] = row.th.a.string
        for col in cols:
            key = col["data-stat"]
            if key in link_fields:
                value = col.a.string
            else:
                value = col.string
            if key in int_fields:
                value = int(value) if value is not None else value
            game_info[key] = value
        games.append(ScheduleGame(**game_info))

    log.debug("parsed info for %u games" % len(games))
    return games


def _parse_game_page_for_team(soup, team):
    stats = []
    # leave the following fields as strings
    str_fields = ["mp"]
    # convert the following fields to floats, remaining fields are ints
    float_fields = ["fg_pct", "fg3_pct", "ft_pct"]

    table = soup.find("table", id="box-%s-game-basic" % team)
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if not cols or ("class" in row and row["class"] == "thead"):
            continue
        # grab the player for the row
        player_link = row.th.a
        # no link for header rows
        if player_link is None:
            continue
        player_stats = {"player": player_link.string}
        # if there is only a single data column, then the player did not play
        if len(cols) == 1:
            stats.append(Player(**player_stats))
            continue
        for col in cols:
            key = col["data-stat"]
            value = col.string
            if key in str_fields:
                pass
            elif key in float_fields:
                value = 0.0 if value is None else float(value)
            else:
                value = 0 if value is None else int(value)
            player_stats[key] = value
        stats.append(Player(**player_stats))

    return stats


def parse_game_page(sched_game, content):
    """
    Parses the game statistics from the web page.

    Arguments:
        sched_game : ScheduleGame object for the game
        content    : HTML content string

    Returns:
        a Game object
    """
    game = {}
    soup = bs4.BeautifulSoup(content, "html.parser")

    # parse stats for players on the away team
    game["away_team"] = sched_game.away_team_id
    game["away_stats"] = _parse_game_page_for_team(
        soup, sched_game.away_team_id)
    # parse stats for players on the home team
    game["home_team"] = sched_game.home_team_id
    game["home_stats"] = _parse_game_page_for_team(
        soup, sched_game.home_team_id)

    return Game(**game)
