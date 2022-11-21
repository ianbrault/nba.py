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

from .game import Game
from .team import Team

from .. import utils


class PlayerGameStats:
    """
    Stores player statistics from a specific game.
    """

    def __init__(
        self,
        id=None, ast=None, blk=None, dreb=None, fg3_pct=None, fg3a=None,
        fg3m=None, fg_pct=None, fga=None, fgm=None, ft_pct=None, fta=None,
        ftm=None, game=None, gp=None, min=None, oreb=None, pf=None, pts=None,
        reb=None, stl=None, team=None, turnover=None,
        **kwargs,
    ):
        self.id = id
        self.ast = ast
        self.blk = blk
        self.dreb = dreb
        self.fg3_pct = fg3_pct
        self.fg3a = fg3a
        self.fg3m = fg3m
        self.fg_pct = fg_pct
        self.fga = fga
        self.fgm = fgm
        self.ft_pct = ft_pct
        self.fta = fta
        self.ftm = ftm
        self.game = Game(**game) if game else None
        self.gp = gp
        self.min = utils.min_to_number(min)
        self.oreb = oreb
        self.pf = pf
        self.pts = pts
        self.reb = reb
        self.stl = stl
        self.team = Team(**team) if team else None
        self.turnover = turnover

    def toJSON(self):
        obj = self.__dict__
        obj["game"] = self.game.toJSON()
        obj["team"] = self.team.toJSON()
        return obj

    def is_dnp(self):
        return self.min == 0
