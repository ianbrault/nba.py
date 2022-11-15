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

from .team import Team


class Player:
    """
    Stores player information and statistics.
    """

    def __init__(
        self,
        id=None, first_name=None, last_name=None, position=None, team=None,
        **kwargs,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.team = Team(**team) if team else team

    def toJSON(self):
        obj = self.__dict__
        obj["team"] = self.team.toJSON()
        return obj

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def bio(self):
        """
        Returns a string with basic information for the player including their
        full name, position, and team.
        """
        return "%s - %s (%s)" % (
            self.full_name, self.position, self.team.abbreviation)
