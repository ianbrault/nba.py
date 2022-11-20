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

from nba import Player
from nba import PlayerGameStats
from nba import Team

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
    responses = await utils.await_and_gather(
        api.get_players(session, name=name) for name in args.name)
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


async def get_teams(session):
    teams_json = []
    path = LOCAL_STORAGE / "teams.json"
    # check if the team information is already stored locally
    if path.exists():
        teams_json = storage.load_json(path)
    # otherwise, grab via the API and store locally
    else:
        teams_json = await api.get_all_teams(session)
        storage.store_json(path, teams_json)
    teams = [Team(**obj) for obj in teams_json]
    return teams


async def get_player_game_stats_for_season(session, player_id, season):
    stats_json = []
    path = LOCAL_STORAGE / ("player_%s_games_%s.json" % (player_id, season))
    # always get the current stats if the current season is requested
    is_curr_season = season == utils.get_current_season()
    if not is_curr_season and path.exists():
        stats_json = storage.load_json(path)
    else:
        stats_json = await api.get_player_game_stats(
            session, player_id, season)
        # only flush if a previous season was requested
        if not is_curr_season:
            storage.store_json(path, stats_json)
    stats = [PlayerGameStats(**obj) for obj in stats_json]
    return stats


async def player_season_averages(args, session):
    # search for the given player
    player = await get_player(args, session)
    if player is None:
        return

    # grab the player season averages for the current season
    season = utils.get_current_season()
    # TODO: these averages include DNPs, need to derive the averages ourselves
    averages = await api.get_player_season_averages(session, player.id, season)
    if not averages:
        return

    # print player name/position/team info
    log.info(player.bio())
    # print player season averages
    log.info("%s GP %s MPG" % (averages["games_played"], averages["min"]))
    log.info(
        "%.1f pts %.1f reb %.1f ast"
        % (averages["pts"], averages["reb"], averages["ast"]))
    log.info(
        "%.3f FG%% (%.1f FG / %.1f FGA)"
        % (averages["fg_pct"], averages["fgm"], averages["fga"]))
    log.info(
        "%.3f 3PT%% (%.1f 3PT / %.1f 3PTA)"
        % (averages["fg3_pct"], averages["fg3m"], averages["fg3a"]))
    log.info(
        "%.3f FT%% (%.1f FT / %.1f FTA)"
        % (averages["ft_pct"], averages["ftm"], averages["fta"]))


async def player_game_log(args, session):
    # search for the given player
    player = await get_player(args, session)
    if player is None:
        return

    # grab the player statistics for the current season and previous seasons,
    # as requested by the lookback argument
    curr_season = utils.get_current_season()
    responses = await utils.await_and_gather(
        get_player_game_stats_for_season(session, player.id, season)
        for season in range(curr_season - args.lookback, curr_season + 1))
    game_stats = list(itertools.chain.from_iterable(responses))
    # TODO: need to filter out DNPs

    # print player name/position/team info
    log.info(player.bio())
    # print player stats for each game
    # reverse so the report is newest-to-oldest
    # track the number of games that have been printed and skip over DNPs
    ngames = 0
    for stats in reversed(game_stats):
        if ngames == args.n:
            break
        player_is_home = player.team.id == stats.game.home_team_id
        # TODO: skip if this is a DNP
        # print date/location/opponent for game
        when = stats.game.date_to_datetime().strftime("%m/%d")
        where = "v." if player_is_home else "@ "
        if player_is_home:
            opp = state.team_id_to_abbreviation(stats.game.visitor_team_id)
        else:
            opp = state.team_id_to_abbreviation(stats.game.home_team_id)
        game_bio = "%s %s %s" % (when, where, opp)
        # print player statistics for the game
        # TODO: print more stats
        log.info(
            "%s: %u pts %u reb %u ast"
            % (game_bio, stats.pts, stats.reb, stats.ast))
        ngames += 1


async def run(args, session):
    # load stored NBA player info
    state.set_players(load_players())
    # load NBA teams info
    state.set_teams(await get_teams(session))

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
