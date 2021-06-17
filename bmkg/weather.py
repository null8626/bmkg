from xmltodict import parse
from datetime import datetime
from .area import Area

class Weather:
    __slots__ = ('source', 'production_center', 'areas', 'date')

    def __init__(self, response: str, **settings):
        json = parse(response)["data"]
        issue = json["forecast"]["issue"]

        self.source = json["@source"]
        self.production_center = json["@productioncenter"]
        self.areas = []
        self.date = datetime(
            int(issue["year"]),
            int(issue["month"]),
            int(issue["day"]),
            int(issue["hour"]),
            int(issue["minute"]),
            int(issue["second"])
        )
        
        for area in json["forecast"]["area"]:
            self.areas.append(Area(area, **settings))
    
    def __len__(self) -> int:
        return len(self.areas)

    def __repr__(self) -> str:
        return f"<Weather date={self.date!r} areas=[{len(self)}]>"