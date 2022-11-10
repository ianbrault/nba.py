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

from . import log

import json


def load_json(path):
    """
    Loads JSON data from the given path.

    Arguments:
        path : File path as a pathlib.Path object

    Returns:
        the data from the file or [] if an error occurred
    """
    data = []
    try:
        log.debug("loading data from %s" % path)
        with path.open() as f:
            data = json.loads(f.read())
    except (IOError, OSError) as ex:
        log.error("failed to load data from %s: %s" % (path, ex))
    return data


def store_json(path, data):
    """
    Stores JSON data to the given path.

    Arguments:
        path : File path as a pathlib.Path object
        data : Data to be stored
    """
    try:
        log.debug("storing data to %s" % path)
        with path.open("w") as f:
            f.write(json.dumps(data))
    except (IOError, OSError) as ex:
        log.error("failed to store data to %s: %s" % (path, ex))
