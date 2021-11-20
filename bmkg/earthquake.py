from datetime import datetime, timedelta, timezone
from .constants import TIMEZONE_OFFSETS, DIRECTION
from collections import namedtuple
from typing import Tuple

EarthquakeLocation = namedtuple("EarthquakeLocation", "length direction location")

class EarthquakeFelt:
    __slots__ = ("__data", "__div")

    def __init__(self, data: dict, settings):
        self.__data = data
        self.__div = 1 if settings.metric else 1.609
    
    @property
    def latitude(self) -> float:
        return float(self.__data["point"]["coordinates"].split(", ")[0])
    
    @property
    def longitude(self) -> float:
        return float(self.__data["point"]["coordinates"].split(", ")[1])
    
    @property
    def magnitude(self) -> float:
        return float(self.__data["Magnitude"])
    
    @property
    def depth(self) -> float:
        return float(self.__data["Kedalaman"].split()[0]) // ()
    
    @property
    def description(self) -> str:
        return self.__data.get("Keterangan")
    
    @property
    def felt_at(self) -> tuple:
        return tuple(self.__data["Dirasakan"].lstrip(" ").rstrip(",").split(", "))
    
    @property
    def date(self) -> "datetime":
        return datetime.strptime(self.__data["Tanggal"].split()[0], "%d/%m/%Y-%H:%M:%S") - self.timezone
    
    @property
    def timezone(self) -> "timedelta":
        return timedelta(hours=TIMEZONE_OFFSETS.index(self.__data["Tanggal"].split()[1]) + 7)
    
    def __repr__(self):
        return f"<EarthquakeFelt latitude={self.latitude} longitude={self.longitude} depth={self.depth} description={self.description}>"

class Earthquake:
    __slots__ = ('__data', '__div')

    def __init__(self, data, as_list_element: bool = False, settings = None):
        self.__data = data
        self.__div  = 1.0 if settings.metric else 1.609
    
    @property
    def latitude(self) -> float:
        return float(self.__data["point"]["coordinates"].split(",")[0])
    
    @property
    def longitude(self) -> float:
        return float(self.__data["point"]["coordinates"].split(",")[1])
    
    @property
    def magnitude(self) -> float:
        return float(self.__data["Magnitude"].split()[0])
    
    @property
    def depth(self) -> float:
        return float(self.__data["Kedalaman"].split()[0]) // self.__div
    
    @property
    def tsunami(self) -> bool:
        return "tidak" in self.__data.get("Potensi", "").lower()
        
    @property
    def date(self) -> bool:
        t = self.__data["Tanggal"].split("-")
        date = "-".join(t[:-1]) + "20" + t[2]
        return datetime.strptime(date + self.__data["Jam"].split()[0], "%d-%b%Y%H:%M:%S") - self.timezone
    
    @property
    def timezone(self) -> "timezone":
        return timedelta(hours=TIMEZONE_OFFSETS.index(self.__data["Jam"].split()[1]) + 7)
    
    @property
    def locations(self) -> Tuple[EarthquakeLocation]:
        map_list = map(str.split, filter(lambda x: x[:7] == "Wilayah", self.__data.keys()))
    
        return tuple(map(lambda x: EarthquakeLocation(
            int(x[0]) // self.__div,
            DIRECTION[x[2]],
            x[-1]
        ), map_list))
    
    def __repr__(self) -> str:
        return f"<Earthquake magnitude={self.magnitude} depth={self.depth} tsunami={self.tsunami} locations=[{len(self.locations)}]>"