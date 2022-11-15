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

import operator


class NBAState:
    """
    Global store for NBA information and statistics.
    """
    players = []
    # used to avoid duplication of player objects
    player_ids = set()

    def set_players(self, nba_players):
        self.players = nba_players
        for player in self.players:
            self.player_ids.add(player.id)

    def add_player(self, player):
        if player.id not in self.player_ids:
            self.players.append(player)
            self.player_ids.add(player.id)

    def add_players(self, player_list):
        for player in player_list:
            self.add_player(player)

    def filter_players(self, names):
        """
        Filters the player list based on the given first/last name(s).

        Arguments:
            names : First/last name(s) to filter on, can be a single string or
                    a list of 1 or 2 strings

        Returns:
            a list of matching Player objects
        """
        if not isinstance(names, list):
            names = list(names)

        if len(names) > 1:
            first = names[0].upper()
            last = names[1].upper()
            combinator = operator.__and__
        else:
            first = names[0].upper()
            last = names[0].upper()
            combinator = operator.__or__

        return [
            p for p in self.players
            if combinator(
                p.first_name.upper() == first, p.last_name.upper() == last)]
