"""
The MIT License (MIT)
Copyright (c) 2021-2023 null (https://github.com/null8626)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from typing import Iterable, Optional, Union
from xml.etree.ElementTree import fromstring
from enum import auto

from .earthquake import FeltEarthquake, LatestEarthquake, RecentEarthquake
from .constants import METRIC, VALID_UNITS
from .base import CustomizableUnit
from .forecast import Weather
from .enums import Province
from .errors import Error

class Client(CustomizableUnit):
  """Represents a ``bmkg`` :class:`Client` class."""
  
  __slots__ = ('__session', 'english')
  
  def __init__(
    self,
    *,
    unit: Optional[auto] = METRIC,
    english: bool = False,
    session: Optional[ClientSession] = None
  ):
    """
    Creates the bmkg client object.
    
    Parameters
    ----------
    unit: Optional[:class:`auto`]
      Whether to use the :term:`metric` or :term:`imperial/customary system` (:attr:`IMPERIAL`). Defaults to :attr:`METRIC`.
    english: 
      Whether to use the :term:`english language` (``True``) or the :term:`native indonesian language` (``False``). Defaults to ``False``.
    session: Optional[:class:`ClientSession`]
      Whether to use an existing :term:`aiohttp client session` for requesting or not. Defaults to ``None`` (creates a new one instead)
    
    Raises
    ------
    Error
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
    """
    
    super().__init__(unit, english)
    
    self.__session = session or ClientSession(
      timeout=ClientTimeout(total=5000.0),
      connector=TCPConnector(verify_ssl=False)
    )
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} [{self.__session!r}]>'
  
  async def get_forecast(
    self,
    province: Optional[Union[str, Province]] = Province.INDONESIA,
    *,
    unit: Optional[auto] = None
  ) -> Weather: # yapf: disable
    """|coro|
    Fetches a weather forecast of a specific province.
    
    Parameters
    ----------
    province: Optional[Union[:class:`str`, :class:`Province`]]
      The requested :class:`Province` :class:`Enum` or province name in the form of a :class:`str` for said weather forecast. Defaults to :attr:`Province.INDONESIA`.
    unit: Optional[:class:`auto`]
      Overrides the :term:`metric` or :term:`imperial/customary system` (:attr:`IMPERIAL`) used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    
    Raises
    ------
    Error
      If the specified province is not a valid province :class:`str` or a part of the :class:`Province` :class:`Enum`.
      If the :term:`aiohttp client session` used by the :class:`Client` object is already closed.
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
      If the :class:`Client` cannot send a web request to the web server.
    
    Returns
    -------
    :class:`Weather`
      The requested weather forecast.
    """
    
    if self.__session.closed:
      raise Error('Client is already closed')
    
    province = province if isinstance(province, Province) else Province(province) # yapf: disable
    
    if unit not in VALID_UNITS:
      unit = self._CustomizableUnit__unit
    
    async with self.__session.get(
      f'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-{province.value}.xml'
    ) as resp:
      return Weather(
        fromstring(await resp.text()).find('forecast'), unit, self.english
      )
  
  async def get_felt_earthquakes(
    self,
    *,
    unit: Optional[auto] = None
  ) -> Iterable[FeltEarthquake]: # yapf: disable
    """|coro|
    Fetches the most recent earthquakes regardless of their magnitude.
    
    Parameters
    ----------
    unit: Optional[:class:`auto`]
      Overrides the :term:`metric` or :term:`imperial/customary system` (:attr:`IMPERIAL`) used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    
    Raises
    ------
    Error
      If the :term:`aiohttp client session` used by the :class:`Client` object is already closed.
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
      If the :class:`Client` cannot send a web request to the web server.
    
    Returns
    -------
    Iterable[:class:`FeltEarthquake`]
      The recent earthquakes regardless of their magnitude.
    """
    
    if unit not in VALID_UNITS:
      unit = self._CustomizableUnit__unit
    
    async with self.__session.get(
      'https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json'
    ) as resp:
      json = await resp.json()
      return (
        FeltEarthquake(earthquake, unit, self.english)
        for earthquake in json['Infogempa']['gempa']
      )
  
  async def get_recent_earthquakes(
    self,
    *,
    unit: Optional[auto] = None
  ) -> Iterable[RecentEarthquake]: # yapf: disable
    """|coro|
    Fetches the most recent earthquakes magnitude 5 or higher.
    
    Parameters
    ----------
    unit: Optional[:class:`auto`]
      Overrides the :term:`metric` or :term:`imperial/customary system` (:attr:`IMPERIAL`) used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    
    Raises
    ------
    Error
      If the :term:`aiohttp client session` used by the :class:`Client` object is already closed.
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
      If the :class:`Client` cannot send a web request to the web server.
    
    Returns
    -------
    Iterable[:class:`RecentEarthquake`]
      The recent earthquakes with the magnitude >= 5.0.
    """
    
    if unit not in VALID_UNITS:
      unit = self._CustomizableUnit__unit
    
    async with self.__session.get(
      'https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json'
    ) as resp:
      json = await resp.json()
      return (
        RecentEarthquake(earthquake, unit, self.english)
        for earthquake in json['Infogempa']['gempa']
      )
  
  async def get_latest_earthquake(
    self, *, unit: Optional[auto] = None
  ) -> LatestEarthquake:
    """|coro|
    Fetches the latest earthquake.
    
    Parameters
    ----------
    unit: Optional[:class:`auto`]
      Overrides the :term:`metric` or :term:`imperial/customary system` (:attr:`IMPERIAL`) used by the :class:`Client` object. Defaults to ``None`` (uses the one from the :class:`Client`).
    
    Raises
    ------
    Error
      If the :term:`aiohttp client session` used by the :class:`Client` object is already closed.
      If the ``unit`` argument is not ``None`` and it's also not :attr:`METRIC` or :attr:`IMPERIAL`.
      If the :class:`Client` cannot send a web request to the web server.
    
    Returns
    -------
    :class:`LatestEarthquake`
      The latest earthquake.
    """
    
    if unit not in VALID_UNITS:
      unit = self._CustomizableUnit__unit
    
    async with self.__session.get(
      'https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json'
    ) as resp:
      json = await resp.json()
      return LatestEarthquake(json['Infogempa']['gempa'], unit, self.english)
  
  async def close(self):
    """|coro|
    Closes the :class:`Client` object. Nothing will happen if it's already closed.
    """
    
    if not self.__session.closed:
      await self.__session.close()
  
  async def __aenter__(self):
    """|coro|
    `async with` handler. Does nothing. Returns `self`
    """
    
    return self
  
  async def __aexit__(self, *_, **__):
    """|coro|
    Closes the :class:`Client` object. Nothing will happen if it's already closed.
    """
    
    await self.close()
