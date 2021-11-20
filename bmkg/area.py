from datetime import datetime
from re import compile
from collections import namedtuple
from .constants import WEATHER_CODE, WIND_DIRECTION_CODE
from typing import List

date_regex = compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})$")
AreaHumidity = namedtuple("AreaHumidity", "date value unit")
AreaTemperature = namedtuple("AreaTemperature", "date value")
AreaWindSpeeds = namedtuple("AreaWindSpeeds", "date value ms knots")
AreaWindDirection = namedtuple("AreaWindDirection", "date value text sexa")
AreaForecast = namedtuple("AreaForecast", "date value icon_url")

class Area:
    __slots__ = ('__settings', '__data')

    def __repr__(self) -> str:
        return f"<Area id={self.id} name={self.name} latitude={self.latitude} longitude={self.longitude}>"

    def __init__(self, data, settings):
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
    def humidity(self) -> List[AreaHumidity]:
        return tuple(map(self._parse_humidity, self.__data["parameter"][0]["timerange"]))
    
    @property
    def max_humidity(self) -> List[AreaHumidity]:
        return tuple(map(self._parse_humidity, self.__data["parameter"][1]["timerange"]))
    
    @property
    def min_humidity(self) -> List[AreaHumidity]:
        return tuple(map(self._parse_humidity, self.__data["parameter"][3]["timerange"]))
    
    @property
    def max_temperature(self) -> List[AreaTemperature]:
        return tuple(map(self._parse_temperature, self.__data["parameter"][2]["timerange"]))
    
    @property
    def min_temperature(self) -> List[AreaTemperature]:
        return tuple(map(self._parse_temperature, self.__data["parameter"][4]["timerange"]))
    
    @property
    def temperature(self) -> List[AreaTemperature]:
        return tuple(map(self._parse_temperature, self.__data["parameter"][5]["timerange"]))

    @property
    def wind_speeds(self) -> List[AreaWindSpeeds]:
        return tuple(map(self._parse_wind_speeds, self.__data["parameter"][8]["timerange"]))
    
    @property
    def wind_direction(self) -> List[AreaWindDirection]:
        return tuple(map(self._parse_wind_direction, self.__data["parameter"][7]["timerange"]))
    
    @property
    def forecast(self) -> List[AreaForecast]:
        return tuple(map(self._parse_forecast, self.__data["parameter"][6]["timerange"]))
    
    def _parse_forecast(self, data: dict) -> "AreaForecast":
        date = datetime(*map(int, date_regex.findall(data["@datetime"])[1]))
        a, b = WEATHER_CODE[date["value"]["#text"]]
    
        return AreaForecast(
            date, a, f"https://www.bmkg.go.id/asset/img/icon-cuaca/{b}-{'am' if date.hour < 12 else 'pm'}.png"
        )
    
    def _parse_wind_direction(self, data: dict) -> "AreaWindDirection":
        val = self.data["value"]
        return AreaWindDirection(
            datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
            float(val[0]["#text"]),
            WIND_DIRECTION_CODE[val[1]["#text"]],
            float(val[2]["#text"])
        )
    
    def _parse_temperature(self, data: dict) -> "AreaTemperature":
        return AreaTemperature(
            datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
            float(data["value"][int(not self.__settings.metric)]["#text"])
        )
    
    def _parse_humidity(self, data: dict) -> "AreaHumidity":
        return AreaHumidity(
            datetime(*map(int, date_regex.findall(data["@datetime"])[1])),
            int(data["value"]["#text"]),
            data["value"]["@unit"]
        )
    
    def _parse_wind_speeds(self, data: dict) -> "AreaWindSpeeds":
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