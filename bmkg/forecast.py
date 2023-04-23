"""
The MIT License (MIT)
Copyright (c) 2021-2023 null (https:/github.com/null8626)
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

from xml.etree.ElementTree import Element
from collections import namedtuple
from datetime import datetime
from typing import Iterable
from enum import auto

from .enums import AreaKind, Direction, ForecastKind
from .constants import METRIC, XML_NAMESPACES
from .base import CustomizableUnit

Humidity = namedtuple('Humidity', 'date value')
LowestHumidity = namedtuple('LowestHumidity', 'date value')
HighestHumidity = namedtuple('HighestHumidity', 'date value')
Temperature = namedtuple('Temperature', 'date value')
LowestTemperature = namedtuple('LowestTemperature', 'date value')
HighestTemperature = namedtuple('HighestTemperature', 'date value')
HourlyForecast = namedtuple('HourlyForecast', 'date kind')
WindDirection = namedtuple('WindDirection', 'date degrees direction')
WindSpeed = namedtuple('WindSpeed', 'date knots value')

class Forecast(CustomizableUnit):
  """Represents a single weather forecast for a given location."""
  
  __slots__ = ('__inner',)
  
  def __init__(self, elem: Element, unit: auto, english: bool):
    super().__init__(unit, english)
    
    self.__inner = elem
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} area_name={self.area_name!r} area_kind={self.area_kind!r} latitude={self.latitude!r} longitude={self.longitude!r}>'
  
  @property
  def latitude(self) -> float:
    """:class:`float`: The :term:`latitude`."""
    
    return float(self.__inner.attrib['latitude'])
  
  @property
  def longitude(self) -> float:
    """:class:`float`: The :term:`longitude`."""
    
    return float(self.__inner.attrib['longitude'])
  
  @property
  def area_kind(self) -> AreaKind:
    """:class:`AreaKind`: The kind of this weather forecast's location."""
    
    return AreaKind(self.__inner.attrib['type'])
  
  @property
  def area_name(self) -> str:
    """:class:`str`: This weather forecast's location name."""
    
    xml_lang = 'en_US' if self.english else 'id_ID'
    
    return self.__inner.find(
      f'./name[@xml:lang="{xml_lang}"]', namespaces=XML_NAMESPACES
    ).text
  
  @property
  def humidity(self) -> Iterable[Humidity]:
    """Iterable[:class:`Humidity`]: This weather forecast's humidity values across various timeframes."""
    
    return (
      Humidity(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        int(child.find('value').text)
      ) for child in self.__inner.iterfind('./parameter[@id="hu"]/timerange')
    )
  
  @property
  def lowest_humidity(self) -> Iterable[LowestHumidity]:
    """Iterable[:class:`LowestHumidity`]: This weather forecast's lowest humidity values across various timeframes."""
    
    return (
      LowestHumidity(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        int(child.find('value').text)
      )
      for child in self.__inner.iterfind('./parameter[@id="humin"]/timerange')
    )
  
  @property
  def highest_humidity(self) -> Iterable[HighestHumidity]:
    """Iterable[:class:`HighestHumidity`]: This weather forecast's highest humidity values across various timeframes."""
    
    return (
      HighestHumidity(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        int(child.find('value').text)
      )
      for child in self.__inner.iterfind('./parameter[@id="humax"]/timerange')
    )
  
  @property
  def temperature(self) -> Iterable[Temperature]:
    """Iterable[:class:`Temperature`]: This weather forecast's temperature across various timeframes."""
    
    unit = 'C' if self._CustomizableUnit__unit == METRIC else 'F'
    
    return (
      Temperature(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        float(child.find(f'./value[@unit="{unit}"]').text)
      ) for child in self.__inner.iterfind('./parameter[@id="t"]/timerange')
    )
  
  @property
  def lowest_temperature(self) -> Iterable[LowestTemperature]:
    """Iterable[:class:`LowestTemperature`]: This weather forecast's lowest temperature across various timeframes."""
    
    unit = 'C' if self._CustomizableUnit__unit == METRIC else 'F'
    
    return (
      LowestTemperature(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        float(child.find(f'./value[@unit="{unit}"]').text)
      ) for child in self.__inner.iterfind('./parameter[@id="tmin"]/timerange')
    )
  
  @property
  def highest_temperature(self) -> Iterable[HighestTemperature]:
    """Iterable[:class:`LowestTemperature`]: This weather forecast's highest temperature across various timeframes."""
    
    unit = 'C' if self._CustomizableUnit__unit == METRIC else 'F'
    
    return (
      HighestTemperature(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        float(child.find(f'./value[@unit="{unit}"]').text)
      ) for child in self.__inner.iterfind('./parameter[@id="tmax"]/timerange')
    )
  
  @property
  def hourly(self) -> Iterable[HourlyForecast]:
    """Iterable[:class:`HourlyForecast`]: This weather forecast's hourly forecast."""
    
    return (
      HourlyForecast(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        ForecastKind(child.find('value').text)
      ) for child in
      self.__inner.iterfind('./parameter[@id="weather"]/timerange')
    )
  
  @property
  def wind_direction(self) -> Iterable[WindDirection]:
    """Iterable[:class:`WindDirection`]: This weather forecast's wind direction across various timeframes."""
    
    return (
      WindDirection(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        float(child.find('./value[@unit="deg"]').text),
        Direction(child.find('./value[@unit="CARD"]').text)
      ) for child in self.__inner.iterfind('./parameter[@id="wd"]/timerange')
    )
  
  @property
  def wind_speeds(self) -> Iterable[WindSpeed]:
    """Iterable[:class:`WindSpeed`]: This weather forecast's wind speeds across various timeframes."""
    
    unit = 'KPH' if self._CustomizableUnit__unit == METRIC else 'MPH'
    
    return (
      WindSpeed(
        datetime.strptime(child.attrib['datetime'], '%Y%m%d%H%M'),
        float(child.find('./value[@unit="Kt"]').text),
        float(child.find(f'./value[@unit="{unit}"]').text)
      ) for child in self.__inner.iterfind('./parameter[@id="ws"]/timerange')
    )

class Weather(CustomizableUnit):
  """Represents an array of weather forecasts in a specific time."""
  
  __slots__ = ('__inner',)
  
  def __init__(self, elem: Element, unit: auto, english: bool):
    super().__init__(unit, english)
    
    self.__inner = elem
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'<{self.__class__.__name__} date={self.date!r}>'
  
  @property
  def date(self) -> datetime:
    """:class:`datetime`: The date for this weather forecast."""
    
    return datetime.strptime(
      self.__inner.find('./issue/timestamp').text, '%Y%m%d%H%M%S'
    )
  
  @property
  def forecasts(self) -> Iterable[Forecast]:
    """Iterable[:class:`Forecast`]: Weather forecasts across various areas."""
    
    return (
      Forecast(area, self._CustomizableUnit__unit, self.english)
      for area in self.__inner.iter('area')
    )
