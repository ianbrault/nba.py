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


class Game:
    """
    Stores game information.
    """

    def __init__(
        self,
        id=None, date=None, home_team_id=None, home_team_score=None,
        season=None, visitor_team_id=None, visitor_team_score=None,
        **kwargs,
    ):
        self.id = id
        self.date = date
        self.home_team_id = home_team_id
        self.home_team_score = home_team_score
        self.season = season
        self.visitor_team_id = visitor_team_id
        self.visitor_team_score = visitor_team_score

    def toJSON(self):
        return self.__dict__

    def date_to_datetime(self):
        return datetime.datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%fZ")
