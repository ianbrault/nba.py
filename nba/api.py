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
from . import parse
from . import utils

import calendar

BASE_URL = "https://www.basketball-reference.com"
# for some reason Basketball Reference rejects the default aiohttp user-agent
# but we can work around this by using the requests user-agent instead
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "python-requests/2.28.1",
}


async def get_players(session, season):
    """
    Queries for statistics for all NBA players for the given season.

    Arguments:
        session : aiohttp.ClientSession object
        season  : NBA season year

    Returns:
        a list of player info as JSON objects
    """
    url = "/leagues/NBA_%s_per_game.html" % season
    log.debug(
        "querying %s season players info from %s%s" % (season, BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.text()
        return parse.parse_players_stats_page(data)


async def get_schedule_for_month(session, season, month):
    """
    Queries for NBA matchups for the given season and month.

    Arguments:
        session : aiohttp.ClientSession object
        season  : NBA season year
        month   : Month as an int

    Returns:
        a list of game info as JSON objects
    """
    month_name = calendar.month_name[month]
    url = "/leagues/NBA_%s_games-%s.html" % (season, month_name.lower())
    log.debug(
        "querying %s %s schedule from %s%s" % (month_name, season, BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.text()
        return parse.parse_schedule_page(data)


async def get_game(session, schedule_game):
    """
    Queries for statistics from the given game.

    Arguments:
        session       : aiohttp.ClientSession object
        schedule_game : ScheduleGame object for the game

    Returns:
        a JSON object for the game
    """
    home_team = utils.FULL_NAME_TO_TRICODE[schedule_game.home_team_name]
    url = "/boxscores/%s0%s.html" % (schedule_game.date_key(), home_team)
    log.debug("querying game info from %s%s" % (BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.text()
        return parse.parse_game_page(schedule_game, data)
