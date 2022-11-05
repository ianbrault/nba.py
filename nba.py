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

import aiohttp

import asyncio
import json
import logging
import os
import pathlib
import sys

# storage directory on the local filesystem
LOCAL_STORAGE = pathlib.Path(os.environ["HOME"]) / ".nba"


async def get_teams_info(session):
    info = []
    season = state.get_current_season()
    teams_file = LOCAL_STORAGE / ("teams_%s.json" % season)
    # if the players info is already stored locally, load it
    if teams_file.exists():
        log.debug("loading %s teams info from %s" % (season, teams_file))
        with teams_file.open() as f:
            info = json.loads(f.read())
    # otherwise, query it from the server and store to the file
    else:
        info = await api.get_teams(session, season)
        log.debug("storing %s players info to %s" % (season, teams_file))
        with teams_file.open("w") as f:
            f.write(json.dumps(info))
    return info


async def get_players_info(session):
    info = []
    season = state.get_current_season()
    players_file = LOCAL_STORAGE / ("players_%s.json" % season)
    # if the players info is already stored locally, load it
    if players_file.exists():
        log.debug("loading %s players info from %s" % (season, players_file))
        with players_file.open() as f:
            info = json.loads(f.read())
    # otherwise, query it from the server and store to the file
    else:
        info = await api.get_players(session, season)
        log.debug("storing %s players info to %s" % (season, players_file))
        with players_file.open("w") as f:
            f.write(json.dumps(info))
    return info


async def player_report(args, session):
    # filter player info for the given player
    log.debug("filtering for player with name(s): %s" % ", ".join(args.name))
    matches = state.filter_players(args.name)
    if len(matches) > 1:
        log.error(
            "ERROR: multiple player matches for name \"%s\""
            % " ".join(args.name))
        match_names = [
            "%s %s" % (p["firstName"], p["lastName"]) for p in matches]
        log.info("select one of the following:\n%s" % "\n".join(match_names))
        sys.exit(1)

    player_info = matches[0]
    # print player name/position/team info
    full_name = "%s %s" % (player_info["firstName"], player_info["lastName"])
    team_tricode = state.team_id_to_tricode(player_info["teamId"])
    log.info("%s - %s (%s)" % (full_name, player_info["pos"], team_tricode))


async def run(args, session):
    # get current NBA info and add to global state
    state.set_nba_info(await api.get_nba_info(session))
    # get NBA teams info and add to global state
    state.set_teams(await get_teams_info(session))
    # get NBA players info and add to global state
    state.set_players(await get_players_info(session))

    if args.command == "report":
        await player_report(args, session)


async def main(args):
    # create the local storage directory, if it does not already exist
    LOCAL_STORAGE.mkdir(exist_ok=True)
    # open the HTTP session and catch exceptions at the top level
    try:
        async with aiohttp.ClientSession(
            base_url=api.BASE_URL, raise_for_status=True,
        ) as session:
            await run(args, session)
    except aiohttp.ClientResponseError as ex:
        log.error("ERROR: failed to retrieve data from the server: %s" % ex)


if __name__ == "__main__":
    try:
        args = cli.parse_args(sys.argv[1:])
        if args.debug:
            log.setLevel(logging.DEBUG)
        asyncio.run(main(args))
    except KeyboardInterrupt:
        pass
