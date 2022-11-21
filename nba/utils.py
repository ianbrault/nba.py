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

import asyncio
import datetime


async def await_and_gather(iterable):
    """
    Execute and gather all promises in the given iterable.

    Arguments:
        iterable : Iterable of futures

    Returns:
        the values returned by the futures, as a nested list or as a flat list
        if the chain argument is set
    """
    return await asyncio.gather(*list(iterable))


def get_date_key():
    """
    Gets a unique identifier for the current date in the format YYYYMMDD.

    Returns:
        the date key as a str
    """
    now = datetime.datetime.now()
    return "%u%02u%02u" % (now.year, now.month, now.day)


def get_current_season():
    """
    Gets the year for the current season. For use by Basketball Reference, this
    is the year of the former half of the season i.e. return 2022 for the
    2022-23 season.

    Returns:
        the current season as an int
    """
    now = datetime.datetime.now()
    year = now.year
    # use April as the end of the (regular) season
    if now.month <= 4:
        year -= 1
    return year


def min_to_number(mp):
    """
    Converts the given minutes played stat from clock format to a number.

    Arguments:
        mp : Minutes played in clock time i.e. 12:34

    Returns:
        the minutes played as a floating-point number
    """
    if not mp:
        mp = 0.0
    elif isinstance(mp, str) and ":" in mp:
        sec = int(mp.split(":")[0])
        subsec = int(mp.split(":")[1])
        mp = sec + (subsec / 60)
    else:
        mp = float(mp)
    return mp


def print_table(logger, table, pad=2):
    """
    Prints tabular data.

    Arguments:
        logger : Logger function, needs to be passed as an argument to avoid a
                 circular import issue
        table  : A 2D list of rows/columns
        pad    : Padding between each column
    """
    sep = " " * pad
    ncols = max(len(row) for row in table)
    col_sizes = [max(len(row[i]) for row in table) for i in range(ncols)]
    for row in table:
        cols = []
        for col, size in zip(row, col_sizes):
            cols.append(col.rjust(size))
        logger(sep.join(cols))
