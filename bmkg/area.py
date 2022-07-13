from datetime import datetime
from enum import Enum
from re import compile
from collections import namedtuple
from typing import Tuple
from .settings import BMKGSettings

date_regex = compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})$")
AreaHumidity = namedtuple("AreaHumidity", "date value unit")
AreaTemperature = namedtuple("AreaTemperature", "date value")
AreaWindSpeeds = namedtuple("AreaWindSpeeds", "date value ms knots")
AreaWindDirection = namedtuple("AreaWindDirection", "date value text sexa")
AreaForecast = namedtuple("AreaForecast", "date value icon_url")

class WindDirection(Enum):
  North = None
  Northeast = None
  East = None
  Southeast = None
  Southwest = None
  West = None
  South = None
  Northwest = None
  Fluctuate = None

  def new(text: str):
    match text:
      case "N":
        return WindDirection.North
      case "NE":
        return WindDirection.Northeast
      case "E":
        return WindDirection.East
      case "SE":
        return WindDirection.Southeast
      case "SW":
        return WindDirection.Southwest
      case "W":
        return WindDirection.West
      case "S":
        return WindDirection.South
      case "NW":
        return WindDirection.Northwest
      case "VARIABLE":
        return WindDirection.Fluctuate

def _parse_humidity(data: dict) -> AreaHumidity:
  return AreaHumidity(
    datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
    int(data["value"]["#text"]),
    data["value"]["@unit"]
  )

class Area:
  __slots__ = ('__settings', '__data')

  def __repr__(self) -> str:
    return f"<Area id={self.id} name={self.name} latitude={self.latitude} longitude={self.longitude}>"

  def __init__(self, data, settings: BMKGSettings):
    self.__settings = settings
    self.__data = data
    
  @property
  def id(self) -> int:
    return int(self.__data["@id"])
  
  @property
  def name(self) -> str:
    return self.__data["name"][int(not self.__settings.english)]["#text"]
  
  @property
  def latitude(self) -> float:
    return float(self.__data["@latitude"])
  
  @property
  def longitude(self) -> float:
    return float(self.__data["@longitude"])
    
  @property
  def type(self) -> str:
    return self.__data["@type"]
  
  @property
  def level(self) -> int:
    return int(self.__data["@level"])
  
  @property
  def humidity_type(self) -> str:
    return self.__data["parameter"][0]["timerange"][0]["@type"]
  
  @property
  def url(self) -> str:
    return f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg?AreaID={self.id}"
  
  @property  
  def humidity(self) -> Tuple[AreaHumidity]:
    return tuple(map(_parse_humidity, self.__data["parameter"][0]["timerange"]))
  
  @property
  def max_humidity(self) -> Tuple[AreaHumidity]:
    return tuple(map(_parse_humidity, self.__data["parameter"][1]["timerange"]))
  
  @property
  def min_humidity(self) -> Tuple[AreaHumidity]:
    return tuple(map(_parse_humidity, self.__data["parameter"][3]["timerange"]))
  
  @property
  def max_temperature(self) -> Tuple[AreaTemperature]:
    return tuple(map(self._parse_temperature, self.__data["parameter"][2]["timerange"]))
  
  @property
  def min_temperature(self) -> Tuple[AreaTemperature]:
    return tuple(map(self._parse_temperature, self.__data["parameter"][4]["timerange"]))
  
  @property
  def temperature(self) -> Tuple[AreaTemperature]:
    return tuple(map(self._parse_temperature, self.__data["parameter"][5]["timerange"]))

  @property
  def wind_speeds(self) -> Tuple[AreaWindSpeeds]:
    return tuple(map(self._parse_wind_speeds, self.__data["parameter"][8]["timerange"]))
  
  @property
  def wind_direction(self) -> Tuple[AreaWindDirection]:
    return tuple(map(self._parse_wind_direction, self.__data["parameter"][7]["timerange"]))
  
  @property
  def forecast(self) -> Tuple[AreaForecast]:
    return tuple(map(self._parse_forecast, self.__data["parameter"][6]["timerange"]))
  
  def _parse_forecast(self, data: dict) -> AreaForecast:
    date = datetime(*map(int, date_regex.findall(data["@datetime"])[1]))
    a, b = (None, None)

    match date["value"]["#text"]:
      case "0":
        a = "Clear Skies"
        b = "cerah"
      case "1":
        a = "Partly Cloudy"
        b = "cerah%20berawan"
      case "2":
        a = "Partly Cloudy"
        b = "cerah%20berawan"
      case "3":
        a = "Mostly Cloudy"
        b = "berawan"
      case "4":
        a = "Overcast"
        b = "berawan%20tebal"
      case "5":
        a = "Haze"
        b = "udara%20kabur"
      case "10":
        a = "Smoke"
        b = "asap"
      case "45":
        a = "Fog"
        b = "kabut"
      case "60":
        a = "Light Rain"
        b = "hujan%20ringan"
      case "61":
        a = "Rain"
        b = "hujan%20sedang"
      case "63":
        a = "Heavy Rain"
        b = "hujan%20lebat"
      case "80":
        a = "Isolated Shower"
        b = "hujan%20lokal"
      case "95":
        a = "Severe Thunderstorm"
        b = "hujan%20petir"
      case "97":
        a = "Severe Thunderstorm"
        b = "hujan%20petir"
      case "100":
        a = "Clear Skies"
        b = "cerah"
      case "101":
        a = "Partly Cloudy"
        b = "cerah%20berawan"
      case "102":
        a = "Partly Cloudy"
        b = "cerah%20berawan"
      case "103":
        a = "Mostly Cloudy"
        b = "berawan"
      case "104":
        a = "Overcast"
        b = "berawan%20tebal"
  
    return AreaForecast(
      date, a, f"https://www.bmkg.go.id/asset/img/icon-cuaca/{b}-{'am' if date.hour < 12 else 'pm'}.png"
    )
  
  def _parse_wind_direction(self, data: dict) -> AreaWindDirection:
    val = self.data["value"]

    return AreaWindDirection(
      datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
      float(val[0]["#text"]),
      WindDirection.new(val[1]["#text"]),
      float(val[2]["#text"])
    )
  
  def _parse_temperature(self, data: dict) -> AreaTemperature:
    return AreaTemperature(
      datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
      float(data["value"][int(not self.__settings.metric)]["#text"])
    )
  
  def _parse_wind_speeds(self, data: dict) -> AreaWindSpeeds:
    val = data["value"]
    
    return AreaWindSpeeds(
      datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
      float(val[int(self.__settings.metric) + 1]["#text"]),
      float(val[3]["#text"]),
      float(val[0]["#text"])
    )
  
  def __int__(self) -> int:
    """ Returns the area ID. """
    return self.id