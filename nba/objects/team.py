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


class Team:
    """
    Stores team information.
    """

    def __init__(
        self,
        id=None, abbreviation=None, city=None, conference=None, division=None,
        full_name=None, name=None,
        **kwargs,
    ):
        self.id = id
        self.abbreviation = abbreviation
        self.city = city
        self.conference = conference
        self.division = division
        self.full_name = full_name
        self.name = name

    def toJSON(self):
        return self.__dict__