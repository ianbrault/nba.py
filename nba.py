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

from nba import Player

import aiohttp

import asyncio
import itertools
import logging
import os
import pathlib
import sys

# storage directory on the local filesystem
LOCAL_STORAGE = pathlib.Path(os.environ["HOME"]) / ".nba"


def load_players():
    players = []
    path = LOCAL_STORAGE / "players.json"
    if path.exists():
        players_json = storage.load_json(path)
        players = [Player(**obj) for obj in players_json]
    return players


def store_players(players):
    path = LOCAL_STORAGE / "players.json"
    players_json = [player.toJSON() for player in players]
    storage.store_json(path, players_json)


async def get_player(args, session):
    player = None
    log.debug("searching for player: %s" % " ".join(args.name))
    # check if the player is already stored in the state
    players = state.filter_players(args.name)
    if len(players) == 1:
        return players[0]
    # otherwise query the API to grab the missing player or any matches that
    # are not already stored in the state
    promises = []
    for name in args.name:
        promises.append(api.get_players(session, name=name))
    responses = await asyncio.gather(*promises)
    players.extend(
        Player(**obj) for obj in itertools.chain.from_iterable(responses))
    # add all players to the state and then re-filter
    state.add_players(players)
    matches = state.filter_players(args.name)
    # check if the player was not found
    if not matches:
        log.error("failed to find player \"%s\"" % " ".join(args.name))
    # check if there are too many matches
    elif len(matches) > 1:
        log.error("multiple player matches for \"%s\"" % " ".join(args.name))
        match_names = [player.full_name for player in matches]
        log.info("select one of the following:\n%s" % "\n".join(match_names))
    # otherwise we found a single matching player
    else:
        player = matches[0]
    return player


async def player_season_averages(args, session):
    # search for the given player
    player = await get_player(args, session)
    if player is None:
        return

    # print player name/position/team info
    log.info(player.bio())
    # # print player season averages
    # log.info("%.1f pts" % player.pts_per_g)
    # log.info(
    #     "%.3f FG%% (%.1f FG / %.1f FGA)"
    #     % (player.fg_pct_per_g, player.fg_per_g, player.fga_per_g))
    # log.info(
    #     "%.3f 3PT%% (%.1f 3PT / %.1f 3PTA)"
    #     % (player.fg3_pct_per_g, player.fg3_per_g, player.fg3a_per_g))
    # log.info(
    #     "%.3f FT%% (%.1f FT / %.1f FTA)"
    #     % (player.ft_pct_per_g, player.ft_per_g, player.fta_per_g))
    # log.info("%.1f reb" % player.trb_per_g)
    # log.info("%.1f ast" % player.ast_per_g)


async def player_game_log(args, session):
    # search for the given player
    player = await get_player(args, session)
    if player is None:
        return

    # # filter player info for the given player
    # player = find_player_by_name(args.name)
    # team_id = player.team_id
    # # grab all played games for the player, we will sub-filter afterwards
    # # this gives ample margin to skip over DNPs
    # player_schedule = state.filter_schedule(team_id)
    # # grab info from games
    # game_info_promises = [get_game(session, g) for g in player_schedule]
    # game_info = await asyncio.gather(*game_info_promises)

    # print player name/position/team info
    log.info(player.bio())
    # # print player stats for each game
    # # reverse so the report is newest-to-oldest
    # # track the number of games that have been printed and skip over DNPs
    # ngames = 0
    # for sched, game in reversed(list(zip(player_schedule, game_info))):
    #     if ngames == args.n:
    #         break
    #     # print date/location/opponent for game
    #     where = "v." if game.is_home_team(player.team_id) else "@ "
    #     game_bio = "%s %s %s" % (
    #         sched.date_str_brief(), where, game.opponent_id(player.team_id))
    #     # get player stats for the game
    #     stats = game.get_player_stats(player)
    #     if stats is None:
    #         # DNP, skip this game
    #         continue
    #     log.info(
    #         "%s: %u pts (%.3f FG%% %u FGA) %u reb %u ast"
    #         % (game_bio, stats.pts, stats.fg_pct, stats.fga, stats.trb,
    #            stats.ast))
    #     ngames += 1


async def run(args, session):
    # load any stored NBA player info
    state.set_players(load_players())

    if args.command == "avg":
        await player_season_averages(args, session)
    if args.command == "games":
        await player_game_log(args, session)

    # flush NBA player info to local storage
    store_players(state.players)


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
