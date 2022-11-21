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

import collections


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

    @staticmethod
    def average(stats_list, filter_dnp=False):
        """
        Derive an average of the list of given statistics.

        Arguments:
            stats_list : List of PlayerGameStats objects to average
            filter_dnp : Filter out games that are classified as DNPs

        Returns:
            a PlayerGameStats object containing the averages
        """
        # filter out DNPs, if requested
        if filter_dnp:
            stats_list = [game for game in stats_list if not game.is_dnp()]
        # convert each object to JSON
        ngames = len(stats_list)
        stats_json = [game.toJSON() for game in stats_list]
        # combine averages
        skip_keys = ["id", "fg3_pct", "fg_pct", "ft_pct", "game", "gp", "team"]
        averages_json = collections.defaultdict(float)
        for game in stats_json:
            for key, value in game.items():
                if key in skip_keys:
                    continue
                averages_json[key] += value
        averages_json = {k: v / ngames for k, v in averages_json.items()}
        # include the additional "games played" key
        averages_json["gp"] = ngames
        return PlayerGameStats(**averages_json)
