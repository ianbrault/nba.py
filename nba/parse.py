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
                if value is None:
                    value = 0.0
                else:
                    value = float(value)
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
        a list of parsed Game objects
    """
    games = []
    soup = bs4.BeautifulSoup(content, "html.parser")
    # the following fields have values wrapped inside links
    link_fields = ["date_game", "visitor_team_name", "home_team_name"]

    table = soup.find("table", id="schedule")
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if not cols or ("class" in row and row["class"] == "thead"):
            continue
        game_info = {}
        # date is in a th, remaining data is in td's
        try:
            game_info[row.th["data-stat"]] = row.th.a.string
        except AttributeError as ex:
            print(row)
            raise ex
        for col in cols:
            key = col["data-stat"]
            if key in link_fields:
                value = col.a.string
            else:
                value = col.string
            game_info[key] = value
        games.append(ScheduleGame(**game_info))

    log.debug("parsed info for %u games" % len(games))
    return games
