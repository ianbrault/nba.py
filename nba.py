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

from nba import Game
from nba import Player
from nba import ScheduleGame

import aiohttp

import asyncio
import itertools
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


async def get_schedule_for_season(session, season):
    schedule = []
    local_file = LOCAL_STORAGE / ("schedule_%s.json" % season)
    # check if the schedule for the season is already stored locally
    if local_file.exists():
        schedule_json = storage.load_json(local_file)
        schedule = [ScheduleGame(**obj) for obj in schedule_json]
    # otherwise, grab via the API and store locally
    else:
        schedule = await api.get_schedule_for_season(session, season)
        schedule_json = [g.toJSON() for g in schedule]
        storage.store_json(local_file, schedule_json)
    # sort chronologically before returning
    schedule = list(sorted(schedule, key=lambda g: g.date_to_datetime()))
    return schedule


async def get_schedule(args, session):
    curr_season = utils.get_current_season()
    # get the schedule for the current and previous seasons, as requested
    season = curr_season - args.lookback
    # wait for all month schedules concurrently
    promises = []
    while season <= curr_season:
        promises.append(get_schedule_for_season(session, season))
        season += 1
    # await all and flatten into a single list
    return itertools.chain.from_iterable(await asyncio.gather(*promises))


async def get_game(session, sched_game):
    game = None
    fname = "game_%s_%s_%s.json" % (
        sched_game.date_key(), sched_game.away_team_id,
        sched_game.home_team_id)
    local_file = LOCAL_STORAGE / fname
    # check if the game is already stored locally
    if local_file.exists():
        game_json = storage.load_json(local_file)
        game = Game.fromJSON(game_json)
    # otherwise, grab via the API and store locally
    else:
        game = await api.get_game(session, sched_game)
        storage.store_json(local_file, game.toJSON())
    return game


def find_player_by_name(names):
    # filter player info for the given player
    log.debug("filtering for player with name(s): %s" % ", ".join(names))
    matches = state.filter_players(names)
    if not matches:
        log.error("failed to find player with name \"%s\"" % " ".join(names))
        sys.exit(1)
    elif len(matches) > 1:
        log.error(
            "multiple player matches for name \"%s\"" % " ".join(names))
        match_names = [player.full_name for player in matches]
        log.info("select one of the following:\n%s" % "\n".join(match_names))
        sys.exit(1)

    return matches[0]


def player_season_averages(args):
    # filter player info for the given player
    player = find_player_by_name(args.name)

    # print player name/position/team info
    log.info(player.bio())
    # print player season averages
    log.info("%.1f pts" % player.pts_per_g)
    log.info(
        "%.3f FG%% (%.1f FG / %.1f FGA)"
        % (player.fg_pct_per_g, player.fg_per_g, player.fga_per_g))
    log.info(
        "%.3f 3PT%% (%.1f 3PT / %.1f 3PTA)"
        % (player.fg3_pct_per_g, player.fg3_per_g, player.fg3a_per_g))
    log.info(
        "%.3f FT%% (%.1f FT / %.1f FTA)"
        % (player.ft_pct_per_g, player.ft_per_g, player.fta_per_g))
    log.info("%.1f reb" % player.trb_per_g)
    log.info("%.1f ast" % player.ast_per_g)


async def player_game_log(args, session):
    # filter player info for the given player
    player = find_player_by_name(args.name)
    team_id = player.team_id
    # grab all played games for the player, we will sub-filter afterwards
    # this gives ample margin to skip over DNPs
    player_schedule = state.filter_schedule(team_id)
    # grab info from games
    game_info_promises = [get_game(session, g) for g in player_schedule]
    game_info = await asyncio.gather(*game_info_promises)

    # print player name/position/team info
    log.info(player.bio())
    # print player stats for each game
    # reverse so the report is newest-to-oldest
    # track the number of games that have been printed and skip over DNPs
    ngames = 0
    for sched, game in reversed(list(zip(player_schedule, game_info))):
        if ngames == args.n:
            break
        # print date/location/opponent for game
        where = "v." if game.is_home_team(player.team_id) else "@ "
        game_bio = "%s %s %s" % (
            sched.date_str_brief(), where, game.opponent_id(player.team_id))
        # get player stats for the game
        stats = game.get_player_stats(player)
        if stats is None:
            # DNP, skip this game
            continue
        log.info(
            "%s: %u pts (%.3f FG%% %u FGA) %u reb %u ast"
            % (game_bio, stats.pts, stats.fg_pct, stats.fga, stats.trb,
               stats.ast))
        ngames += 1


async def run(args, session):
    # get NBA players info and add to global state
    players_info = await get_players(session)
    state.set_players(players_info)
    # get NBA schedule and add to global state
    schedule_info = await get_schedule(args, session)
    state.set_schedule(schedule_info)

    if args.command == "avg":
        player_season_averages(args)
    if args.command == "games":
        await player_game_log(args, session)


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
