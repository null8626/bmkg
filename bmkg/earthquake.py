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

from datetime import datetime, timedelta, timezone
from collections import namedtuple
from typing import Iterable
from enum import auto

from .constants import AFFECTED_REGION_REGEX, METRIC
from .base import CustomizableUnit
from .enums import MMI

AffectedRegion = namedtuple('AffectedRegion', 'mmi region')

_TIMEZONE_OFFSET = {"B": 7, "A": 8, "T": 9}

class RecentEarthquake(CustomizableUnit):
  """Represents a recent earthquake with a magnitude >= 5.0."""
  
  __slots__ = ('__inner',)
  
  def __init__(self, inner: dict, unit: auto, english: bool):
    super().__init__(unit, english)
    
    self.__inner = inner
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} date={self.date!r} latitude={self.latitude!r} longitude={self.longitude!r} magnitude={self.magnitude!r} depth={self.depth!r}>'
  
  @property
  def date(self) -> datetime:
    """:class:`datetime`: The date when this earthquake happened in UTC."""
    
    return datetime.fromisoformat(self.__inner['DateTime'])
  
  @property
  def local_date(self) -> datetime:
    """:class:`datetime`: The date when this earthquake happened in the local timezone."""
    
    return self.date.astimezone(
      timezone(timedelta(hours=_TIMEZONE_OFFSET[self.__inner['Jam'][-1]]))
    )
  
  @property
  def depth(self) -> float:
    """:class:`float`: The depth of this earthquake in either Kilometers or Miles."""
    
    kms = float(self.__inner['Kedalaman'][:-3])
    
    return kms if self._CustomizableUnit__unit == METRIC else kms / 1.609
  
  @property
  def magnitude(self) -> float:
    """:class:`float`: This earthquake's magnitude."""
    
    return float(self.__inner['Magnitude'])
  
  @property
  def latitude(self) -> float:
    """:class:`float`: This earthquake's epicenter latitude."""
    
    return float(self.__inner['Lintang'][:-3])
  
  @property
  def longitude(self) -> float:
    """:class:`float`: This earthquake's epicenter longitude."""
    
    return float(self.__inner['Bujur'][:-3])

class FeltEarthquake(RecentEarthquake):
  """Represents a recent earthquake (any magnitude)."""
  
  __slots__ = ()
  
  def __init__(self, inner: dict, unit: auto, english: bool):
    super().__init__(inner, unit, english)
  
  @property
  def affected_regions(self) -> Iterable[AffectedRegion]:
    """Iterable[:class:`AffectedRegion`]: Weather forecasts across various areas."""
    
    for region in self._RecentEarthquake__inner['Dirasakan'].split(', '):
      _, mmi, name = AFFECTED_REGION_REGEX.findall(region)[0]
      
      yield AffectedRegion(MMI(mmi), name)

class LatestEarthquake(FeltEarthquake):
  """Represents the latest earthquake."""
  
  __slots__ = ()
  
  def __init__(self, inner: dict, unit: auto, english: bool):
    super().__init__(inner, unit, english)
  
  @property
  def shake_map(self) -> str:
    """:class:`str`: A URL to this earthquake's shake map image."""
    
    return f'https://data.bmkg.go.id/DataMKG/TEWS/{self._RecentEarthquake__inner["Shakemap"]}'
