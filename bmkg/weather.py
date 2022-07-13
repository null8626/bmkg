from xmltodict import parse
from datetime import datetime
from .settings import BMKGSettings
from .area import Area

class Weather:
  __slots__ = ('__json', '__settings')

  def __init__(self, response: str, settings: BMKGSettings):
    self.__json = parse(response)["data"]
    self.__settings = settings
  
  @property
  def areas(self) -> tuple:
    return tuple(map(lambda x: Area(x, self.__settings), self.__json["forecast"]["area"]))
  
  @property
  def production_center(self) -> str:
    return self.__json["@productioncenter"]
  
  @property
  def source(self) -> str:
    return self.__json["@source"]
  
  @property
  def date(self) -> datetime:
    issue = self.__json["forecast"]["issue"]
    
    return datetime(
      int(issue["year"]),
      int(issue["month"]),
      int(issue["day"]),
      int(issue["hour"]),
      int(issue["minute"]),
      int(issue["second"])
    )
  
  def __len__(self) -> int:
    return len(self.areas)

  def __repr__(self) -> str:
    return f"<Weather date={self.date!r} areas=[{len(self)!r}]>"