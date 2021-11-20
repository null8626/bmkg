# from .weather import Weather
# from .constants import PROVINCES
from .earthquake import Earthquake, EarthquakeFelt

from collections import namedtuple
from aiohttp import ClientSession
from datetime import datetime
from typing import Tuple

BMKGSettings = namedtuple("BMKGSettings", "english metric")

class BMKG:
    __slots__ = ('__settings', 'session')

    def __repr__(self) -> str:
        return f"<BNKG [closed]>" if self.session.closed else f"<BMKG english={self.__settings.english} metric={self.__settings.metric}>"

    def __init__(self, english: bool = False, metric: bool = True, session: "ClientSession" = None) -> None:
        """
        BMKG wrapper for Python.
        """
        
        self.__settings = BMKGSettings(english, metric)
        self.session = session or ClientSession()

    async def get_forecast(self, location: str = None) -> "Weather":
        """ Fetches the forecast for a specific location. """
        raise DeprecationWarning("This feature is deprecated due to an unfixable server bug.")
        # if not location:
        #     return await self._handle_request(PROVINCES["indonesia"])
        # 
        # location = location.lower().replace(" ", "_").replace("di", "dki").replace("jogja", "yogya").lstrip("provinsi ")
        # if location in PROVINCES:
        #     return await self._handle_request(PROVINCES[location])
        # 
        # for province in PROVINCES:
        #     if location in province:
        #         return await self._handle_request(PROVINCES[province])
        # 
        # return await self._handle_request(PROVINCES["indonesia"])

    async def get_climate_info(self) -> bytes:
        """ Fetches the climate information image. """
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/CEWS/pch/pch.bulan.1.cond1.png")
        return await response.read()
    
    async def get_satellite_image(self) -> bytes:
        """ Fetches the satellite image. """
        response = await self.session.get("https://inderaja.bmkg.go.id/IMAGE/HIMA/H08_EH_Indonesia.png")
        return await response.read()
    
    async def get_wave_height_forecast(self) -> bytes:
        """ Fetches the wave height forecast image. """
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/MEWS/maritim/gelombang_maritim.png")
        return await response.read()

    async def get_wind_forecast(self) -> bytes:
        """ Fetches the wind forecast. """
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/MEWS/angin/streamline_d1.jpg")
        return await response.read()
    
    async def get_forest_fires(self) -> bytes:
        """ Fetches the current forest fires. """
        response = await self.session.get("https://cdn.bmkg.go.id/DataMKG/MEWS/spartan/36_indonesia_ffmc_01.png")
        return await response.read()
    
    async def get_recent_earthquake_map(self) -> bytes:
        """ Fetches the recent earthquakes map. """
        response = await self.session.get("https://data.bmkg.go.id/eqmap.gif")
        return await response.read()

    async def get_recent_earthquake(self) -> "Earthquake":
        response = await self.session.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")
        result = await response.json()
        
        return Earthquake(result["Infogempa"]["gempa"], settings=self.__settings)

    async def get_earthquakes_felt(self) -> Tuple[EarthquakeFelt]:
        """ Fetches the recent earthquakes felt. """
        response = await self.session.get("https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json")
        result = await response.json()
        
        return tuple(map(lambda earthquake: EarthquakeFelt(earthquake, settings=self.__settings), result["Infogempa"]["gempa"]))

    async def get_recent_earthquakes(self) -> Tuple[Earthquake]:
        """ Fetches the recent earthquakes. """
        response = await self.session.get("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json")
        result = await response.json()
        
        return tuple(map(lambda earthquake: Earthquake(earthquake, settings=self.__settings), result["Infogempa"]["gempa"]))

    # async def _handle_request(self, xml_path: str) -> "Weather":
    #     """ Handles a request. """
    #     response = await self.session.get(f"https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-{xml_path}.xml")
    #     text = await response.text()
    #     return Weather(text, self.__settings)
    
    async def close(self) -> None:
        """ Closes the session. """
        if self.session.closed:
            return
        
        await self.session.close()