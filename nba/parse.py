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
from .player import Player

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

    table = soup.find("table", id="per_game_stats")
    for row in table.find_all("tr", class_="full_table"):
        player_info = {}
        for col in row.find_all("td"):
            key = col["data-stat"]
            if key == "player" or key == "team_id":
                value = col.a.string
            else:
                value = col.string
            player_info[key] = value
        players.append(Player(**player_info))

    log.debug("parsed info for %u players" % len(players))
    return players
