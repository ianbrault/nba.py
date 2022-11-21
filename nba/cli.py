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

import argparse


def add_subparser(subparsers, command, description=""):
    """
    Adds a subparser to the subparsers object and automatically assigns common
    arguments, including -d/--debug.

    Arguments:
        subparsers  : ArgumentParser subparsers object
        command     : Subparser sub-command
        description : Subparser description

    Returns:
        the subparser object
    """
    subparser = subparsers.add_parser(command, description=description)
    subparser.add_argument(
        "-d", "--debug", action="store_true",
        help="Enable debug output.")
    return subparser


def parse_args(args):
    """
    Parses command-line arguments

    Arguments:
        args : Command-line argument array

    Returns:
        parsed argparse object
    """
    parser = argparse.ArgumentParser(
        description="Queries useful NBA statistics.")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command")

    averages_subparser = add_subparser(
        subparsers, "avg",
        description="Reports season averages for the given player.")
    averages_subparser.add_argument(
        "name", nargs="+",
        help="Player name, specify first/last/both as needed")

    games_subparser = add_subparser(
        subparsers, "games",
        description="Reports stats from the last 5 games for the given "
        "player.")
    games_subparser.add_argument(
        "name", nargs="+",
        help="Player name, specify first/last/both as needed")
    games_subparser.add_argument(
        "-b", dest="basic", action="store_true",
        help="Log only a basic points/rebounds/assists slashline")
    games_subparser.add_argument(
        "-l", dest="lookback", metavar="SEASONS", type=int, default=1,
        help="Lookback to grab games from previous seasons")
    games_subparser.add_argument(
        "-n", dest="ngames", metavar="GAMES", type=int, default=5,
        help="Number of games")
    games_subparser.add_argument(
        "-o", dest="opponent", metavar="TEAM",
        help="Opponent")

    return parser.parse_args(args)
