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


class ScheduleGame:
    """
    Stores schedule game information.
    """

    def __init__(
        self,
        date_game=None, game_start_time=None, visitor_team_name=None,
        home_team_name=None,
        **kwargs,
    ):
        self.date_game = date_game
        self.game_start_time = game_start_time
        self.visitor_team_name = visitor_team_name
        self.home_team_name = home_team_name

    def toJSON(self):
        return self.__dict__

    def date_to_datetime(self):
        return datetime.datetime.strptime(self.date_game, "%a, %b %d, %Y")
