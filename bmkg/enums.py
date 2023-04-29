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

from typing import Optional, Union

from .base import BasicEnum
from .constants import PROVINCE_PREFIX_REGEX
from .errors import Error

class AreaKind(BasicEnum):
  """Represents kinds of areas."""
  
  __slots__ = ()
  
  LAND = 'land'
  SEA = 'sea'

class Province(BasicEnum):
  """Represents a list of indonesian provinces."""
  
  __slots__ = ()
  
  ACEH = "Aceh"
  BALI = "Bali"
  BANGKA_BELITUNG = "BangkaBelitung"
  BANTEN = "Banten"
  BENGKULU = "Bengkulu"
  YOGYAKARTA = "DIYogyakarta"
  JAKARTA = "DKIJakarta"
  GORONTALO = "Gorontalo"
  JAMBI = "Jambi"
  WEST_JAVA = "JawaBarat"
  CENTRAL_JAVA = "JawaTengah"
  EAST_JAVA = "JawaTimur"
  WEST_KALIMANTAN = "KalimantanBarat"
  SOUTH_KALIMANTAN = "KalimantanSelatan"
  CENTRAL_KALIMANTAN = "KalimantanTengah"
  EAST_KALIMANTAN = "KalimantanTimur"
  NORTH_KALIMANTAN = "KalimantanUtara"
  RIAU_ISLANDS = "KepulauanRiau"
  LAMPUNG = "Lampung"
  MALUKU = "Maluku"
  NORTH_MALUKU = "MalukuUtara"
  WEST_NUSA_TENGGARA = "NusaTenggaraBarat"
  EAST_NUSA_TENGGARA = "NusaTenggaraTimur"
  PAPUA = "Papua"
  WEST_PAPUA = "PapuaBarat"
  RIAU = "Riau"
  WEST_SULAWESI = "SulawesiBarat"
  SOUTH_SULAWESI = "SulawesiSelatan"
  CENTRAL_SULAWESI = "SulawesiTengah"
  SOUTHEAST_SULAWESI = "SulawesiTenggara"
  NORTH_SULAWESI = "SulawesiUtara"
  WEST_SUMATERA = "SumateraBarat"
  SOUTH_SUMATERA = "SumateraSelatan"
  NORTH_SUMATERA = "SumateraUtara"
  INDONESIA = "Indonesia"
  
  @classmethod
  def _missing_(self, name: Optional[str]):
    if name is None:
      return self.INDONESIA
    
    name = PROVINCE_PREFIX_REGEX.sub('', name.lower().lstrip()).replace(' ', '')
    
    for e in Province:
      n = e.name.lower()
      v = e.value.lower()
      
      if n == name or n == v:
        return e
    
    raise Error(f'"{name}" is not a valid province name.')

class Direction(BasicEnum):
  """Represents a wind direction."""
  
  __slots__ = ()
  
  NORTH = "N"
  NORTH_NORTHEAST = "NNE"
  NORTHEAST = "NE"
  EAST_NORTHEAST = "ENE"
  EAST = "E"
  EAST_SOUTHEAST = "ESE"
  SOUTHEAST = "SE"
  SOUTH_SOUTHEAST = "SSE"
  SOUTH = "S"
  SOUTH_SOUTHWEST = "SSW"
  SOUTHWEST = "SW"
  WEST_SOUTHWEST = "WSW"
  WEST = "W"
  WEST_NORTHWEST = "WNW"
  NORTHWEST = "NW"
  NORTH_NORTHWEST = "NNW"
  FLUCTUATE = "VARIABLE"
  
  def __contains__(self, degrees: Union[float, int]) -> bool:
    """
    Checks if the degrees value is a part of this wind direction.
    
    Parameters
    ----------
    degrees: Union[:class:`float`, :class:`int`]
      The degrees value. Must be between 0 and 360.
    
    Raises
    ------
    Error
      Invalid ``degrees`` argument.
    
    Returns
    -------
    :class:`bool`
      The boolean.
    """
    
    if not ((isinstance(degrees, int) or isinstance(degrees, float)) and 0 <= degrees <= 360): # yapf: disable
      raise Error('Invalid degrees value.')
    elif self is self.NORTH:
      return degrees > 348.75 or degrees <= 11.25
    elif self is self.NORTH_NORTHEAST:
      return 11.25 < degrees <= 33.75
    elif self is self.NORTHEAST:
      return 33.75 < degrees <= 56.25
    elif self is self.EAST_NORTHEAST:
      return 56.25 < degrees <= 78.75
    elif self is self.EAST:
      return 78.75 < degrees <= 101.25
    elif self is self.EAST_SOUTHEAST:
      return 101.25 < degrees <= 123.75
    elif self is self.SOUTHEAST:
      return 123.75 < degrees <= 146.25
    elif self is self.SOUTH_SOUTHEAST:
      return 146.25 < degrees <= 168.75
    elif self is self.SOUTH:
      return 168.75 < degrees <= 191.25
    elif self is self.SOUTH_SOUTHWEST:
      return 191.25 < degrees <= 213.75
    elif self is self.SOUTHWEST:
      return 213.75 < degrees <= 236.25
    elif self is self.WEST_SOUTHWEST:
      return 236.25 < degrees <= 258.75
    elif self is self.WEST:
      return 258.75 < degrees <= 281.25
    elif self is self.WEST_NORTHWEST:
      return 281.25 < degrees <= 303.75
    elif self is self.NORTHWEST:
      return 303.75 < degrees <= 326.25
    else:
      return 326.25 < degrees <= 348.75

class ForecastKind(BasicEnum):
  """Represents a weather forecast kind."""
  
  __slots__ = ()
  
  CLEAR_SKIES = "0"
  PARTLY_CLOUDY = "1"
  MOSTLY_CLOUDY = "3"
  OVERCAST = "4"
  HAZE = "5"
  SMOKE = "10"
  FOG = "45"
  LIGHT_RAIN = "60"
  RAIN = "61"
  HEAVY_RAIN = "63"
  ISOLATED_SHOWER = "80"
  SEVERE_THUNDERSTORM = "95"
  
  @classmethod
  def _missing_(self, name: str):
    if name == "2":
      return WeatherKind.PARTLY_CLOUDY
    elif name == "97":
      return WeatherKind.SEVERE_THUNDERSTORM

class MMI(BasicEnum):
  """Represents an earthquake's MMI (Modified Mercalli Intensity) scale."""
  
  __slots__ = ()
  
  NOT_FELT = "I"
  WEAK = "II"
  LIGHT = "IV"
  MODERATE = "V"
  STRONG = "VI"
  VERY_STRONG = "VII"
  SEVERE = "VIII"
  VIOLENT = "IX"
  EXTREME = "X"
  
  @classmethod
  def _missing_(self, value: str):
    if value == "III":
      return self.WEAK
    elif value == "XI" or value == "XII":
      return self.EXTREME