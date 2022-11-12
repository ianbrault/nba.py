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

from .player import Player


class Game:
    """
    Stores game statistics.
    """

    def __init__(
        self,
        away_team=None, away_stats=None, home_team=None, home_stats=None,
        **kwargs,
    ):
        self.away_team = away_team
        self.away_stats = away_stats
        self.home_team = home_team
        self.home_stats = home_stats

    def toJSON(self):
        return {
            "away_team": self.away_team,
            "away_stats": [p.toJSON() for p in self.away_stats],
            "home_team": self.home_team,
            "home_stats": [p.toJSON() for p in self.home_stats],
        }

    @staticmethod
    def fromJSON(obj):
        away_stats = [Player(**o) for o in obj["away_stats"]]
        home_stats = [Player(**o) for o in obj["home_stats"]]
        return Game(
            away_team=obj["away_team"], away_stats=away_stats,
            home_team=obj["home_team"], home_stats=home_stats,
        )

    def is_home_team(self, team_id):
        return team_id == self.home_team

    def opponent_id(self, team_id):
        if self.is_home_team(team_id):
            return self.away_team
        else:
            return self.home_team

    def get_player_stats(self, player):
        if self.is_home_team(player.team_id):
            team_stats = self.home_stats
        else:
            team_stats = self.away_stats
        stats = [p for p in team_stats if p.player == player.player]
        return stats[0] if stats else None

