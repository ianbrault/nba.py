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

import datetime


def get_current_season():
    """
    Gets the year for the current season. For use by Basketball Reference, this
    is the year of the latter half of the season i.e. return 2023 for the
    2022-23 season.

    Returns:
        the current season as an int
    """
    now = datetime.datetime.now()
    year = now.year
    # use October as the start of the season
    if now.month >= 10:
        year += 1
    return year
