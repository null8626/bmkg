from datetime import datetime, timedelta, timezone
from enum import Enum
from collections import namedtuple

from .settings import BMKGSettings

class Direction(Enum):
  southwest = None
  northwest = None
  southeast = None
  northeast = None
  north = None
  south = None
  east = None
  west = None

  def new(text: str):
    match text:
      case "BaratDaya":
        return Direction.southwest
      case "BaratLaut":
        return Direction.northwest
      case "Tenggara":
        return Direction.southeast
      case "TimurLaut":
        return Direction.northeast
      case "Utara":
        return Direction.north
      case "Selatan":
        return Direction.south
      case "Timur":
        return Direction.east
      case "Barat":
        return Direction.west

def get_timezone_offset(name: str) -> int:
  match name:
    case "WIB":
      return 7
    case "WITA":
      return 8
    case "WIT":
      return 9

EarthquakeLocation = namedtuple("EarthquakeLocation", "distance direction location")

class EarthquakeFelt:
  __slots__ = ("__data", "__date")

  def __init__(self, data: dict):
    self.__data = data
    self.__date = data["Tanggal"].split()

  @property
  def latitude(self) -> str:
    return self.__data["Lintang"]
  
  @property
  def longitude(self) -> str:
    return self.__data["Bujur"]
  
  @property
  def magnitude(self) -> float:
    return float(self.__data["Magnitude"])
  
  @property
  def depth(self) -> float:
    return float(self.__data["Kedalaman"].split()[0])
  
  @property
  def description(self) -> str:
    return self.__data.get("Keterangan")
  
  @property
  def felt_at(self) -> tuple:
    return tuple(self.__data["Dirasakan"].lstrip(" ").rstrip(",").split(", "))
  
  @property
  def date(self) -> datetime:
    return datetime.strptime(self.__date[0], "%d/%m/%Y-%H:%M:%S") - self.timezone
  
  @property
  def timezone(self) -> timedelta:
    return timedelta(hours=get_timezone_offset(self.__date[1]))
  
  def __repr__(self) -> str:
    return f"<EarthquakeFelt depth={self.depth} description={self.description}>"

class Earthquake:
  __slots__ = ('__data', '__div')

  def __init__(self, data, settings: BMKGSettings):
    self.__data = data
    self.__div = 1.0 if settings.metric else 1.609
  
  @property
  def magnitude(self) -> float:
    return float(self.__data["Magnitude"].split()[0])
  
  @property
  def depth(self) -> float:
    return float(self.__data["Kedalaman"].split()[0]) // self.__div
  
  @property
  def tsunami(self) -> bool:
    return "tidak" not in self.__data.get("Potensi", "").lower()
    
  @property
  def date(self) -> datetime:
    t = self.__data["Tanggal"].split("-")
    date = "-".join(t[:-1]) + "20" + t[2]
    return datetime.strptime(date + self.__data["Jam"].split()[0], "%d-%b%Y%H:%M:%S") - self.timezone
  
  @property
  def timezone(self) -> timezone:
    return timedelta(hours=get_timezone_offset(self.__data["Jam"].split()[1]))
  
  @property
  def location(self) -> EarthquakeLocation:
    split = self.__data["Wilayah"].split()

    return EarthquakeLocation(
      int(split[0]) // self.__div,
      Direction.new(split[2]),
      split[-1]
    )
  
  def __repr__(self) -> str:
    return f"<Earthquake magnitude={self.magnitude} depth={self.depth} tsunami={self.tsunami} location={self.location}>"