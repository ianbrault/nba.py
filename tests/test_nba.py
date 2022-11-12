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
import pytest


def test_version():
    assert __version__ == "0.2.0"


def aio_session():
    return aiohttp.ClientSession(
        base_url=api.BASE_URL, headers=api.HEADERS, raise_for_status=True)


@pytest.mark.asyncio
async def test_api_players():
    season = 2023
    async with aio_session() as session:
        players = await api.get_players(session, season)
        assert len(players) > 0


@pytest.mark.asyncio
async def test_api_schedule_for_month():
    season = 2023
    months = [11, 12, 3]
    async with aio_session() as session:
        for month in months:
            games = await api.get_schedule_for_month(session, season, month)
            assert len(games) > 0


@pytest.mark.asyncio
async def test_api_game():
    season = 2023
    month = 10
    async with aio_session() as session:
        games = await api.get_schedule_for_month(session, season, month)
        game = await api.get_game(session, games[-1])
        assert bool(game)
