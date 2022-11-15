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

from . import utils

import operator


class NBAState:
    """
    Global store for NBA information and statistics.
    """
    players = []
    schedule = []

    def set_players(self, nba_players):
        self.players = nba_players

    def set_schedule(self, nba_schedule):
        self.schedule = nba_schedule

    def filter_players(self, names):
        """
        Filters the player list based on the given first/last name(s).

        Arguments:
            names : First/last name(s) to filter on, can be a single string or
                    a list of 1 or 2 strings

        Returns:
            a list of matching player objects
        """
        # players must be set
        if not self.players:
            raise RuntimeError("NBAState.players has not been set")
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

    def filter_schedule(self, team_id, played=True):
        """
        Filters the schedule for games based on the given team tricode.

        Arguments:
            team_id : Team tricode
            played  : Only include games that have already been played

        Returns:
            a list of matching game objects
        """
        # schedule must be set
        if not self.schedule:
            raise RuntimeError("NBAState.schedule has not been set")

        team = utils.TRICODE_TO_FULL_NAME[team_id]
        games = [
            g for g in self.schedule
            if g.home_team_name == team or g.visitor_team_name == team]
        # further filter by games that have already been played, if requested
        if played:
            games = [g for g in games if g.is_played()]
        return games
