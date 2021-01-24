from xmltodict import parse
from datetime import datetime
from .area import Area

class Weather:
    def __init__(self, response, **settings):
        json = parse(response)["data"]
        self.source = json["@source"]
        self.production_center = json["@productioncenter"]
        self.areas = []
        self.date = datetime(
            int(json["forecast"]["issue"]["year"]),
            int(json["forecast"]["issue"]["month"]),
            int(json["forecast"]["issue"]["day"]),
            int(json["forecast"]["issue"]["hour"]),
            int(json["forecast"]["issue"]["minute"]),
            int(json["forecast"]["issue"]["second"])
        )
        
        for area in json["forecast"]["area"]:
            self.areas.append(Area(area, **settings))
    
    def __repr__(self):
        return f"<Weather date={repr(self.date)} areas=[{len(self.areas)}]>"