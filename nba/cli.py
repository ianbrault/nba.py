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
    subparsers = parser.add_subparsers(help="Sub-command")

    report_subparser = subparsers.add_parser(
        "report",
        description="Produce a report for the given player, including basic "
        "player info, season averages, and game log.")
    report_subparser.add_argument(
        "name", nargs="+",
        help="Player name, specify first/last/both as needed")

    return parser.parse_args(args)
