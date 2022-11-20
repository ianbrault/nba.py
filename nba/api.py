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

import asyncio
import collections
import itertools

BASE_URL = "https://www.balldontlie.io"
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "python-requests/2.28.1",
}
RESULTS_PER_PAGE = 100


def build_url(base, **kwargs):
    """
    Builds a URL query string given the base stem and query parameters.

    Arguments:
        base   : Base URL
        kwargs : Query parameters

    Returns:
        the URL string
    """
    if not kwargs:
        return base
    param_strs = []
    for key, value in kwargs.items():
        is_iter = isinstance(value, collections.abc.Iterable)
        is_str = isinstance(value, str)
        if is_iter and not is_str:
            for val in value:
                param_strs.append("%s[]=%s" % (key, val))
        else:
            param_strs.append("%s=%s" % (key, value))
    return "%s?%s" % (base, "&".join(param_strs))


async def get_json(session, url, data=False,**kwargs):
    """
    Performs a GET request for JSON data.

    Arguments:
        session : aiohttp.ClientSession object
        url     : Full URL string
        data    : Only return the data payload, excluding the meta payload
        kwargs  : Query parameters

    Returns:
        the retrieved JSON data, or {} if an error was encountered
    """
    url = build_url(url, **kwargs)
    log.debug("query: %s%s" % (BASE_URL, url))
    async with session.get(url) as rsp:
        rsp = await rsp.json()
        if data:
            rsp = rsp["data"]
        return rsp


async def get_paginated(session, base_url, **kwargs):
    """
    Performs a series of GET requests for paginated data.

    Arguments:
        session  : aiohttp.ClientSession object
        base_url : Base URL
        kwargs   : Query parameters (excluding pagination arguments)

    Returns:
        the paginated data as JSON
    """
    data = []
    # perform the initial request
    args = kwargs.copy()
    args["per_page"] = RESULTS_PER_PAGE
    req = await get_json(session, base_url, **args)
    data.extend(req["data"])
    # check if there are any further pages
    next_page = req["meta"]["next_page"]
    if not next_page:
        return data
    # perform requests for remaining pages concurrently
    promises = []
    for page in range(next_page, req["meta"]["total_pages"] + 1):
        args["page"] = page
        promises.append(get_json(session, base_url, **args))
    # await all requests and combine results
    responses = await asyncio.gather(*promises)
    data.extend(
        itertools.chain.from_iterable(rsp["data"] for rsp in responses))
    return data


async def get_players(session, name=None):
    """
    Retrieves information for all NBA players.

    Arguments:
        session : aiohttp.ClientSession object
        name    : Filter on the player first/last name

    Returns:
        a list of player info as JSON objects
    """
    url = "/api/v1/players"
    args = {}
    if name:
        args["search"] = name
    # data is paginated
    return await get_paginated(session, url, **args)


async def get_all_teams(session):
    """
    Retrieves information for all NBA teams.

    Arguments:
        session : aiohttp.ClientSession object

    Returns:
        a list of team info as JSON objects
    """
    url = "/api/v1/teams"
    # data is paginated
    return await get_paginated(session, url)


async def get_player_season_averages(session, player_id, season):
    """
    Retrieves season averages for the given NBA player.

    Arguments:
        session   : aiohttp.ClientSession object
        player_id : Player ID
        season    : NBA season

    Returns:
        the player averages as a JSON object
    """
    url = "/api/v1/season_averages"
    args = {"season": season, "player_ids": [player_id]}
    rsp = await get_json(session, url, **args, data=True)
    return rsp[0] if rsp else None


async def get_player_game_stats(session, player_id, seasons):
    """
    Retrieves game statistics for the given NBA player from the provided NBA
    season(s).

    Arguments:
        session   : aiohttp.ClientSession object
        player_id : Player ID
        seasons   : NBA season(s) can be an int or a list

    Returns:
        the player averages as a JSON object
    """
    if not isinstance(seasons, collections.abc.Iterable):
        seasons = [seasons]
    url = "/api/v1/stats"
    args = {"seasons": seasons, "player_ids": [player_id]}
    # data is paginated
    return await get_paginated(session, url, **args)
