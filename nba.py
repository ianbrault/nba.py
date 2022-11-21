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
import collections
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


def get_team(key):
    team = None
    log.debug("searching for team: %s" % key)
    # search for the team in the state
    matches = state.filter_teams(key)
    # check if the team was not found
    if not matches:
        log.error("failed to find team \"%s\"" % key)
    # check if there are too many matches
    elif len(matches) > 1:
        log.error("multiple team matches for \"%s\"" % " ".join(key))
        match_names = [
            "%s (%s)" % (team.full_name, team.abbreviation)
            for team in matches]
        log.info("select one of the following:\n%s" % "\n".join(match_names))
    # otherwise we found a single matching team
    else:
        team = matches[0]
    return team


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


async def get_player_season_averages(session, player_id):
    # get the player game stats for the current season
    season = utils.get_current_season()
    season_stats = await get_player_game_stats_for_season(
        session, player_id, season)
    # combine the averages and filter out DNPs
    return PlayerGameStats.average(season_stats, filter_dnp=True)


async def player_season_averages(args, session):
    # search for the given player
    player = await get_player(args, session)
    if player is None:
        return

    # grab the player season averages for the current season
    averages = await get_player_season_averages(session, player.id)
    if not averages:
        return
    # derive shooting percentages manually
    fg_pct = (averages.fgm / averages.fga) * 100
    fg3_pct = (averages.fg3m / averages.fg3a) * 100
    ft_pct = (averages.ftm / averages.fta) * 100

    # print player name/position/team info
    log.info(player.bio())
    # print player season averages
    log.info("%s GP %0.1f MPG" % (averages.gp, averages.min))
    log.info(
        "%.1f pts %.1f reb %.1f ast"
        % (averages.pts, averages.reb, averages.ast))
    log.info(
        "%.1f%% FG (%.1f FGM / %.1f FGA)"
        % (fg_pct, averages.fgm, averages.fga))
    log.info(
        "%.1f%% 3PT (%.1f 3PTM / %.1f 3PTA)"
        % (fg3_pct, averages.fg3m, averages.fg3a))
    log.info(
        "%.1f%% FT (%.1f FT / %.1f FTA)"
        % (ft_pct, averages.ftm, averages.fta))


async def player_game_log(args, session):
    # search for the given player
    player = await get_player(args, session)
    if player is None:
        return
    # search for the given opponent, if provided
    opponent = None
    if args.opponent is not None:
        opponent = get_team(args.opponent)
        if opponent is None:
            return

    # grab the player statistics for the current season and previous seasons,
    # as requested by the lookback argument
    curr_season = utils.get_current_season()
    responses = await utils.await_and_gather(
        get_player_game_stats_for_season(session, player.id, season)
        for season in range(curr_season - args.lookback, curr_season + 1))
    game_stats = list(itertools.chain.from_iterable(responses))
    # sort chronologically
    game_stats = sorted(game_stats, key=lambda g: g.game.date_to_datetime())

    # print player name/position/team info
    log.info(player.bio())

    # print game log as tabular data
    table = []
    # track the objects for each game so that they can be averaged and that the
    # logging stops after the correct number of games have been logged
    games = []
    # print player stats for each game
    # reverse so the report is newest-to-oldest
    for stats in reversed(game_stats):
        if len(games) >= args.ngames:
            break
        # skip the game if it is a DNP
        if stats.is_dnp():
            continue
        # check which team is the player team and which is the opponent
        player_is_home = player.team.id == stats.game.home_team_id
        if player_is_home:
            opponent_id = stats.game.visitor_team_id
        else:
            opponent_id = stats.game.home_team_id
        # if the opponent was specified, skip games that do not involve them
        if opponent is not None and opponent.id != opponent_id:
            continue
        # print as columns
        cols = []
        # print date/location/opponent for game
        when = stats.game.date_to_datetime().strftime("%m/%d/%Y")
        where = "v." if player_is_home else "@ "
        who = state.team_id_to_abbreviation(opponent_id)
        cols.append("%s %s%s" % (when, where, who))
        # print player statistics for the game
        cols.append("%u pts" % stats.pts)
        cols.append("%u reb" % stats.reb)
        cols.append("%u ast" % stats.ast)
        # only print points/rebounds/assists if basic flag is given
        if not args.basic:
            cols.append("%u-%u FG" % (stats.fgm, stats.fga))
            cols.append("%u-%u 3PT" % (stats.fg3m, stats.fg3a))
            cols.append("%u-%u FT" % (stats.ftm, stats.fta))
        table.append(cols)
        games.append(stats)
    # derive the averages for the games and log
    averages_row = ["AVERAGES"]
    averages = PlayerGameStats.average(games)
    averages_row.append("%.1f" % averages.pts)
    averages_row.append("%.1f" % averages.reb)
    averages_row.append("%.1f" % averages.ast)
    # only print points/rebounds/assists if basic flag is given
    if not args.basic:
        averages_row.append("%.1f%%" % ((averages.fgm / averages.fga) * 100))
        averages_row.append("%.1f%%" % ((averages.fg3m / averages.fg3a) * 100))
        averages_row.append("%.1f%%" % ((averages.ftm / averages.fta) * 100))
    table.append(averages_row)
    # print the game log
    utils.print_table(log.info, table)


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
