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

from typing import Optional, Self
from enum import Enum

from .constants import PROVINCE_PREFIX_REGEX
from .errors import Error

class AreaKind(Enum):
  """Represents kinds of areas."""
  
  __slots__ = ()
  
  LAND = 'land'
  SEA = 'sea'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.title()

class Province(Enum):
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
  def _missing_(self, name: Optional[str]) -> Self:
    if name is None:
      return self.INDONESIA
    
    name = PROVINCE_PREFIX_REGEX.sub('', name.lower().lstrip()).replace(' ', '')
    
    for e in Province:
      n = e.name.lower()
      v = e.value.lower()
      
      if n == name or n == v:
        return e
    
    raise Error(f'"{name}" is not a valid province name.')

class Direction(Enum):
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
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()

class ForecastKind(Enum):
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
  def _missing_(self, name: str) -> Self:
    if name == "2":
      return WeatherKind.PARTLY_CLOUDY
    elif name == "97":
      return WeatherKind.SEVERE_THUNDERSTORM
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()

class MMI(Enum):
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
  def _missing_(self, value: str) -> Self:
    if value == "III":
      return MMI.WEAK
    elif value == "XI" or value == "XII":
      return MMI.EXTREME
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()
