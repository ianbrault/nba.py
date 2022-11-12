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

from .nba_state import NBAState
from .objects.game import Game
from .objects.player import Player
from .objects.schedule import ScheduleGame

import logging

__version__ = "0.2.0"


# initialize global state object
state = NBAState()


class LogFormatter(logging.Formatter):
    """
    Custom logging formatter to add ANSI colors.
    """
    black = "\x1b[30m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    reset = "\x1b[0m"
    # fmt = "[%(asctime)s] %(message)s"
    fmt = "%(message)s"

    FORMATS = {
        logging.DEBUG: green + fmt + reset,
        logging.INFO: black + fmt + reset,
        logging.WARNING: yellow + fmt + reset,
        logging.ERROR: red + fmt + reset,
        logging.CRITICAL: red + fmt + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# initialize global logger object
log = logging.getLogger("nba")
# default to info-level, can be further specified via CLI args
log.setLevel(logging.INFO)
# setup console handler
handler = logging.StreamHandler()
handler.setFormatter(LogFormatter())
log.addHandler(handler)
