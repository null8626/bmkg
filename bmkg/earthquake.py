from datetime import datetime, timedelta, timezone
from xmltodict import parse
from .constants import TIMEZONE_OFFSETS, DIRECTION

class TsunamiEarthquake:
    __slots__ = ('date', 'timezone', 'depth', 'magnitude', 'location', 'url')

    def __init__(self, data, **settings):
        data = parse(data)["Infotsunami"]["Gempa"]
        date = "-".join(data["Tanggal"].split("-")[:-1]) + ("20" + data["Tanggal"].split("-")[2])
        self.date = datetime.strptime(date + data["Jam"].split()[0], "%d-%b%Y%H:%M:%S") - timedelta(hours=TIMEZONE_OFFSETS[data["Jam"].split()[1]])
        self.timezone = timezone(timedelta(hours=TIMEZONE_OFFSETS[data["Jam"].split()[1]]))
        
        self.depth = float(data["Kedalaman"].split()[0]) // (1 if settings["metric"] else 1.609)
        self.magnitude = float(data["Magnitude"].split()[0])
        self.location = {
            "length": float(data["Area"].split()[0]) // (1 if settings["metric"] else 1.609),
            "direction": DIRECTION[data["Area"].split()[2]],
            "location": data["Area"].split()[-1]
        }
        self.url = data["Linkdetail"]
    
    def __repr__(self):
        return f"<TsunamiEarthquake magnitude={self.magnitude} depth={self.depth} date={repr(self.date)}>"

class EarthquakeFelt:
    def __init__(self, data: dict, **settings):
        self.latitude    = float(data["point"]["coordinates"].split(", ")[0])
        self.longitude   = float(data["point"]["coordinates"].split(", ")[1])
        self.magnitude   = float(data["Magnitude"])
        self.depth       = float(data["Kedalaman"].split()[0]) // (1 if settings["metric"] else 1.609)
        self.description = data.get("Keterangan")
        self.felt_at     = data["Dirasakan"].lstrip(" ").rstrip(",").split(", ")
        self.date        = datetime.strptime(data["Tanggal"].split()[0], "%d/%m/%Y-%H:%M:%S") - timedelta(hours=TIMEZONE_OFFSETS[data["Tanggal"].split()[1]])
        self.timezone    = timezone(timedelta(hours=TIMEZONE_OFFSETS[data["Tanggal"].split()[1]]))
    
    def __repr__(self):
        return f"<EarthquakeFelt latitude={self.latitude} longitude={self.longitude} depth={self.depth} description={self.description}>"

class Earthquake:
    __slots__ = ('latitude', 'longitude', 'magnitude', 'depth', 'tsunami', 'date', 'timezone', 'locations')

    def __init__(self, data: "str | dict", as_list_element: bool = False, **settings):
        data = data if as_list_element else parse(data)["Infogempa"]["gempa"][0]
        self.latitude = float(data["point"]["coordinates"].split(",")[0])
        self.longitude = float(data["point"]["coordinates"].split(",")[1])
        self.magnitude = float(data["Magnitude"].split()[0])
        self.depth = float(data["Kedalaman"].split()[0]) // (1 if settings["metric"] else 1.609)
        self.tsunami = (data["Potensi"][:5] != "tidak") if data.get("Potensi") else None
        
        date = "-".join(data["Tanggal"].split("-")[:-1]) + ("20" + data["Tanggal"].split("-")[2])
        self.date = datetime.strptime(date + data["Jam"].split()[0], "%d-%b%Y%H:%M:%S") - timedelta(hours=TIMEZONE_OFFSETS[data["Jam"].split()[1]])
        self.timezone = timezone(timedelta(hours=TIMEZONE_OFFSETS[data["Jam"].split()[1]]))
        self.locations = [{
            "length": int(data[i].split()[0]) // (1 if settings["metric"] else 1.609),
            "direction": DIRECTION[data[i].split()[2]],
            "location": data[i].split()[-1]
        } for i in filter(lambda x: x[:7] == "Wilayah", data.keys())]
    
    def __repr__(self) -> str:
        return f"<Earthquake magnitude={self.magnitude} depth={self.depth} tsunami={self.tsunami} locations=[{len(self.locations)}]>"