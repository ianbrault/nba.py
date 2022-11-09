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

BASE_URL = "https://www.basketball-reference.com"
# for some reason Basketball Reference rejects the default aiohttp user-agent
# but we can work around this by using the requests user-agent instead
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "python-requests/2.28.1",
}


async def get_players(session, season):
    """
    Queries for info for all NBA players for the given season.

    Arguments:
        session : aiohttp.ClientSession object
        season  : NBA season year

    Returns:
        player info as a JSON object
    """
    url = "/leagues/NBA_%s_per_game.html" % season
    log.debug("querying %s players info from %s%s" % (season, BASE_URL, url))
    async with session.get(url) as rsp:
        data = await rsp.text()
        return parse.parse_players_stats_page(data)
