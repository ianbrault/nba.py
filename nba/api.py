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

BASE_URL = "http://data.nba.net"


async def get_nba_info(session):
    """
    Queries for current NBA info.

    Arguments:
        session : aiohttp.ClientSession object

    Returns:
        info as a JSON object
    """
    url = "/10s/prod/v1/today.json"
    log.debug("querying NBA info from %s%s" % (BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.json()
        # post-process: remove _internal key
        del data["_internal"]
        return data


async def get_teams(session, season):
    """
    Queries for info for all NBA teams for the given season.

    Arguments:
        session : aiohttp.ClientSession object
        season  : NBA season year

    Returns:
        team info as a JSON object
    """
    url = "/prod/v2/%s/teams.json" % season
    log.debug("querying %s teams info from %s%s" % (season, BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.json()
        return data["league"]["standard"]


async def get_players(session, season):
    """
    Queries for info for all NBA players for the given season.

    Arguments:
        session : aiohttp.ClientSession object
        season  : NBA season year

    Returns:
        player info as a JSON object
    """
    url = "/prod/v1/%s/players.json" % season
    log.debug("querying %s players info from %s%s" % (season, BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.json()
        return data["league"]["standard"]
