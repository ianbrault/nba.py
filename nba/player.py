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

    def __init__(
        self, player=None, pos=None, team_id=None, pts_per_g=None,
        fg_per_g=None, fga_per_g=None, fg3_per_g=None, fg3a_per_g=None,
        ft_per_g=None, fta_per_g=None, **kwargs,
    ):
        self.player = player
        self.pos = pos
        self.team_id = team_id
        self.pts_per_game = pts_per_g
        self.fg_per_game = fg_per_g
        self.fga_per_game = fga_per_g
        self.fg3_per_game = fg3_per_g
        self.fg3a_per_game = fg3a_per_g
        self.ft_per_game = ft_per_g
        self.fta_per_game = fta_per_g

    def toJSON(self):
        return self.__dict__

    @property
    def first_name(self):
        return self.player.split(" ")[0]

    @property
    def last_name(self):
        return " ".join(self.player.split(" ")[1:])

    @property
    def fg_pct(self):
        return self.fg_per_game / self.fga_per_game

    @property
    def fg3_pct(self):
        return self.fg3_per_game / self.fg3a_per_game

    @property
    def ft_pct(self):
        return self.ft_per_game / self.fta_per_game
