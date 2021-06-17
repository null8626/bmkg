from datetime import datetime
from .constants import WEATHER_CODE, WIND_DIRECTION_CODE

class Area:
    __slots__ = (
        '_metric', 'id', 'name', 'latitude', 'longitude', 'type', 'level',
        'humidity_type', 'url', 'humidity', 'max_humidity', 'min_humidity',
        'max_temperature', 'min_temperature', 'temperature', 'wind_speeds',
        'wind_direction', 'forecast'
    )

    def __repr__(self) -> str:
        return f"<Area id={self.id} name={self.name} latitude={self.latitude} longitude={self.longitude}>"

    def __init__(self, data, **settings):
        self._metric = bool(settings.get("metric"))
        self.id = int(data["@id"])
        self.name = data["name"][int(not settings.get("english"))]["#text"]
        self.latitude = float(data["@latitude"])
        self.longitude = float(data["@longitude"])
        self.type = data["@type"]
        self.level = int(data["@level"])
        self.humidity_type = data["parameter"][0]["timerange"][0]["@type"]
        self.url = f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg?AreaID={self.id}"
        
        self.humidity = list(map(self._parse_humidity, data["parameter"][0]["timerange"]))
        self.max_humidity = list(map(self._parse_humidity, data["parameter"][1]["timerange"]))
        self.min_humidity = list(map(self._parse_humidity, data["parameter"][3]["timerange"]))
    
        self.max_temperature = list(map(self._parse_temperature, data["parameter"][2]["timerange"]))
        self.min_temperature = list(map(self._parse_temperature, data["parameter"][4]["timerange"]))
        self.temperature = list(map(self._parse_temperature, data["parameter"][5]["timerange"]))
        
        self.wind_speeds = list(map(lambda x: {
            "datetime": datetime(
                int(x["@datetime"][:4]),
                int(x["@datetime"][4:6]),
                int(x["@datetime"][6:8]),
                int(x["@datetime"][8:10]),
                int(x["@datetime"][10:])
            ),
            "value": float(x["value"][int(self._metric) + 1]["#text"]),
            "ms": float(x["value"][3]["#text"]),
            "knots": float(x["value"][0]["#text"])
        }, data["parameter"][8]["timerange"]))
    
        self.wind_direction = list(map(lambda x: {
            "datetime": datetime(
                int(x["@datetime"][:4]),
                int(x["@datetime"][4:6]),
                int(x["@datetime"][6:8]),
                int(x["@datetime"][8:10]),
                int(x["@datetime"][10:])
            ),
            "value": float(x["value"][0]["#text"]),
            "text": WIND_DIRECTION_CODE[x["value"][1]["#text"]],
            "sexa": float(x["value"][2]["#text"])
        }, data["parameter"][7]["timerange"]))
    
        self.forecast = list(map(lambda x: {
            "datetime": datetime(
                int(x["@datetime"][:4]),
                int(x["@datetime"][4:6]),
                int(x["@datetime"][6:8]),
                int(x["@datetime"][8:10]),
                int(x["@datetime"][10:])
            ),
            "value": WEATHER_CODE[x["value"]["#text"]][0],
            "icon_url": WEATHER_CODE[x["value"]["#text"]][1].format("am" if int(x["@datetime"][8:10]) < 12 else "pm")
        }, data["parameter"][6]["timerange"]))
    
    def _parse_temperature(self, data: dict) -> dict:
        return {
            "datetime": datetime(
                int(data["@datetime"][:4]),
                int(data["@datetime"][4:6]),
                int(data["@datetime"][6:8]),
                int(data["@datetime"][8:10]),
                int(data["@datetime"][10:])
            ),
            "value": float(data["value"][int(not self._metric)]["#text"])
        }
    
    def _parse_humidity(self, data: dict) -> dict:
        return {
            "datetime": datetime(
                int(data["@datetime"][:4]),
                int(data["@datetime"][4:6]),
                int(data["@datetime"][6:8]),
                int(data["@datetime"][8:10]),
                int(data["@datetime"][10:])
            ),
            "value": int(data["value"]["#text"]),
            "unit": data["value"]["@unit"]
        }
    
    def __int__(self) -> int:
        """ Returns the area ID. """
        return self.id