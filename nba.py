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

from nba import api
from nba import cli
from nba import log
from nba import state
from nba import storage
from nba import utils
from nba.player import Player

import aiohttp

import asyncio
import json
import logging
import os
import pathlib
import sys

# storage directory on the local filesystem
LOCAL_STORAGE = pathlib.Path(os.environ["HOME"]) / ".nba"


async def get_players(session):
    players = []
    season = utils.get_current_season()
    date = utils.get_date_key()
    local_file = LOCAL_STORAGE / ("players_%s.json" % date)
    # check if the player info for the current date is already stored locally
    if local_file.exists():
        players_json = storage.load_json(local_file)
        players = [Player(**obj) for obj in players_json]
    # otherwise, grab via the API and store locally
    else:
        players = await api.get_players(session, season)
        players_json = [p.toJSON() for p in players]
        storage.store_json(local_file, players_json)
    return players


def player_season_averages(args):
    # filter player info for the given player
    log.debug("filtering for player with name(s): %s" % ", ".join(args.name))
    matches = state.filter_players(args.name)
    if len(matches) > 1:
        log.error(
            "multiple player matches for name \"%s\"" % " ".join(args.name))
        match_names = [player.full_name for player in matches]
        log.info("select one of the following:\n%s" % "\n".join(match_names))
        sys.exit(1)

    player = matches[0]
    # print player name/position/team info
    log.info("%s - %s (%s)" % (player.player, player.pos, player.team_id))
    log.info("%.1f pts" % player.pts_per_g)
    log.info(
        "%.3f FG%% (%.1f FG / %.1f FGA)"
        % (player.fg_pct, player.fg_per_g, player.fga_per_g))
    log.info(
        "%.3f 3PT%% (%.1f 3PT / %.1f 3PTA)"
        % (player.fg3_pct, player.fg3_per_g, player.fg3a_per_g))
    log.info(
        "%.3f FT%% (%.1f FT / %.1f FTA)"
        % (player.ft_pct, player.ft_per_g, player.fta_per_g))
    log.info("%.1f reb" % player.trb_per_g)
    log.info("%.1f ast" % player.ast_per_g)


async def run(args, session):
    # get NBA players info and add to global state
    players_info = await get_players(session)
    state.set_players(players_info)

    if args.command == "avg":
        player_season_averages(args)


async def main(args):
    # create the local storage directory, if it does not already exist
    LOCAL_STORAGE.mkdir(exist_ok=True)
    # open the HTTP session and catch exceptions at the top level
    try:
        async with aiohttp.ClientSession(
            base_url=api.BASE_URL, headers=api.HEADERS, raise_for_status=True,
        ) as session:
            await run(args, session)
    except aiohttp.ClientResponseError as ex:
        log.error("failed to retrieve data from the server: %s" % ex)


if __name__ == "__main__":
    try:
        args = cli.parse_args(sys.argv[1:])
        if args.debug:
            log.setLevel(logging.DEBUG)
        asyncio.run(main(args))
    except KeyboardInterrupt:
        pass
