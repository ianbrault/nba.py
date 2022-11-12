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
        self,
        player=None,
        # the following are set for season averages
        pos=None, team_id=None, pts_per_g=None, fg_per_g=None, fga_per_g=None,
        fg3_per_g=None, fg3a_per_g=None, ft_per_g=None, fta_per_g=None,
        trb_per_g=None, ast_per_g=None,
        # the following are set for per-game statistics
        mp=None, pts=None, fg=None, fga=None, fg3=None, fg3a=None, ft=None,
        fta=None, trb=None, ast=None,
        **kwargs,
    ):
        self.player = player
        # season averages
        self.pos = pos
        self.team_id = team_id
        self.pts_per_g = pts_per_g
        self.fg_per_g = fg_per_g
        self.fga_per_g = fga_per_g
        self.fg3_per_g = fg3_per_g
        self.fg3a_per_g = fg3a_per_g
        self.ft_per_g = ft_per_g
        self.fta_per_g = fta_per_g
        self.trb_per_g = trb_per_g
        self.ast_per_g = ast_per_g
        # per-game statistics
        self.mp = mp
        self.pts = pts
        self.fg = fg
        self.fga = fga
        self.fg3 = fg3
        self.fg3a = fg3a
        self.ft = ft
        self.fta = fta
        self.trb = trb
        self.ast = ast

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
        return self.fg / self.fga

    @property
    def fg_pct_per_g(self):
        return self.fg_per_g / self.fga_per_g

    @property
    def fg3_pct(self):
        return self.fg3 / self.fg3a

    @property
    def fg3_pct_per_g(self):
        return self.fg3_per_g / self.fg3a_per_g

    @property
    def ft_pct(self):
        return self.ft / self.fta

    @property
    def ft_pct_per_g(self):
        return self.ft_per_g / self.fta_per_g

    def bio(self):
        """
        Returns a string with basic information for the player including their
        full name, position, and team.
        """
        return "%s - %s (%s)" % (self.player, self.pos, self.team_id)
