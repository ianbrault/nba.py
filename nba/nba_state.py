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


class NBAState:
    """
    Global store for NBA information and statistics.
    """
    info = {}
    players = []

    def set_nba_info(self, nba_info):
        self.info = nba_info

    def set_players(self, nba_players):
        self.players = nba_players

    def get_current_season(self):
        # info must be set
        if not self.info:
            raise RuntimeError("NBAState.info has not been set")
        return self.info["seasonScheduleYear"]
