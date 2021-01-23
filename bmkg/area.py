from datetime import datetime
from .constants import WEATHER_CODE, WIND_DIRECTION_CODE

class Area:
    def __repr__(self):
        return f"<Area id={self.id} name={self.name} latitude={self.latitude} longitude={self.longitude}>"

    def __init__(self, data, **settings):
        self._settings       = settings
        self.id              = int(data["@id"])
        self.name            = data["@name"][0 if settings["english"] else 1]["#text"]
        self.latitude        = float(data["@latitude"])
        self.longitude       = float(data["@longitude"])
        self.type            = data["@type"]
        self.level           = int(data["@level"])
        self.humidity_type   = data["parameter"][0]["timerange"][0]["@type"]
        self.url             = f"https://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg?AreaID={self.id}"
                       
        self.humidity        = list(map(self._parse_humidity, data["parameter"][0]["timerange"]))
        self.max_humidity    = list(map(self._parse_humidity, data["parameter"][1]["timerange"]))
        self.min_humidity    = list(map(self._parse_humidity, data["parameter"][3]["timerange"]))
    
        self.max_temperature = list(map(self._parse_temperature, data["parameter"][2]["timerange"]))
        self.min_temperature = list(map(self._parse_temperature, data["parameter"][4]["timerange"]))
        self.temperature     = list(map(self._parse_temperature, data["parameter"][5]["timerange"]))
    
        self.wind_speeds     = list(map(lambda x: {
            "datetime": datetime(
                int(data["@datetime"][:4]),
                int(data["@datetime"][4:6]),
                int(data["@datetime"][6:8]),
                int(data["@datetime"][8:10]),
                int(data["@datetime"][10:])
            ),
            "value": float(data["value"][2 if self._settings["metric"] else 1]["#text"]),
            "ms": float(data["value"][3]),
            "knots": float(data["value"][0])
        }, data["parameter"][7]["timerange"]))
    
        self.wind_direction  = list(map(lambda x: {
            "datetime": datetime(
                int(data["@datetime"][:4]),
                int(data["@datetime"][4:6]),
                int(data["@datetime"][6:8]),
                int(data["@datetime"][8:10]),
                int(data["@datetime"][10:])
            ),
            "value": int(data["value"][0]["#text"]),
            "text": WIND_DIRECTION_CODE[data["value"][1]["#text"]],
            "sexa": int(data["value"][2]["#text"])
        }, data["parameter"][7]["timerange"]))
    
        self.forecast        = list(map(lambda x: {
            "datetime": datetime(
                int(data["@datetime"][:4]),
                int(data["@datetime"][4:6]),
                int(data["@datetime"][6:8]),
                int(data["@datetime"][8:10]),
                int(data["@datetime"][10:])
            ),
            "value": WEATHER_CODE[x["value"]["#text"]]
        }, data["parameter"][7]["timerange"]))
    
    def _parse_temperature(self, data):
        return {
            "datetime": datetime(
                int(data["@datetime"][:4]),
                int(data["@datetime"][4:6]),
                int(data["@datetime"][6:8]),
                int(data["@datetime"][8:10]),
                int(data["@datetime"][10:])
            ),
            "value": float(data["value"][0 if self._settings["metric"] else 1]["#text"])
        }
    
    def _parse_humidity(self, data):
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
    
    def __int__(self):
        return self.id