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

from nba import __version__
from nba import api

import aiohttp


def test_version():
    assert __version__ == "0.3.0"


def aio_session():
    return aiohttp.ClientSession(
        base_url=api.BASE_URL, headers=api.HEADERS, raise_for_status=True)


def test_build_url():
    base_url = "www.foo.bar/baz"
    params = {"a": "X", "b": "Y", "c": "Z"}
    result = api.build_url(base_url, **params)
    assert result.startswith("www.foo.bar/baz?")
    assert "a=X" in result
    assert "b=Y" in result
    assert "c=Z" in result
    assert len([c for c in result if c == "&"]) == 2
