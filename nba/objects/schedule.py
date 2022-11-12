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

from .. import utils

import datetime


class ScheduleGame:
    """
    Stores schedule game information.
    """

    def __init__(
        self,
        date_game=None, game_start_time=None, visitor_team_name=None,
        visitor_pts=None, home_team_name=None, home_pts=None,
        **kwargs,
    ):
        self.date_game = date_game
        self.game_start_time = game_start_time
        self.visitor_team_name = visitor_team_name
        self.visitor_pts = visitor_pts
        self.home_team_name = home_team_name
        self.home_pts = home_pts

    def toJSON(self):
        return self.__dict__

    @property
    def away_team_id(self):
        return utils.FULL_NAME_TO_TRICODE[self.visitor_team_name]

    @property
    def home_team_id(self):
        return utils.FULL_NAME_TO_TRICODE[self.home_team_name]

    def date_to_datetime(self):
        return datetime.datetime.strptime(self.date_game, "%a, %b %d, %Y")

    def date_key(self):
        return self.date_to_datetime().strftime("%Y%m%d")

    def date_str_brief(self):
        time = self.date_to_datetime()
        return "%02u/%02u" % (time.month, time.day)

    def is_played(self):
        return self.visitor_pts is not None and self.home_pts is not None
