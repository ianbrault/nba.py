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


class Player:
    """
    Stores player information and statistics.
    """

    def __init__(self, object):
        self.full_name = object["player"]
        self.first_name = self.full_name.split(" ")[0]
        self.last_name = " ".join(self.full_name.split(" ")[1:])
        self.position = object["pos"]
        self.team = object["team_id"]
        self.pts_per_game = object["pts_per_g"]
        self.fg_per_game = object["fg_per_g"]
        self.fga_per_game = object["fga_per_g"]
        self.fg3_per_game = object["fg3_per_g"]
        self.fg3a_per_game = object["fg3a_per_g"]
        self.ft_per_game = object["ft_per_g"]
        self.fta_per_game = object["fta_per_g"]

    def fg_pct(self):
        return self.fg_per_game / self.fga_per_game

    def fg3_pct(self):
        return self.fg3_per_game / self.fg3a_per_game

    def ft_pct(self):
        return self.ft_per_game / self.fta_per_game
