DIRECTION = {
    "BaratDaya": "southwest",
    "BaratLaut": "northwest",
    "Tenggara": "southeast",
    "TimurLaut": "northeast",
    "Utara": "north",
    "Selatan": "south",
    "Timur": "east",
    "Barat": "west"
}

TIMEZONE_OFFSETS = {
    "WIB": 7,
    "WITA": 8,
    "WIT": 9
}

WIND_DIRECTION_CODE = {
    "N": "North",
    "NNE": "North-Northeast",
    "NE": "Northeast",
    "ENE": "East-Northeast",
    "E": "East",
    "ESE": "East-Southeast",
    "SE": "Southeast",
    "SSE": "South-Southeast",
    "SSW": "South-Southwest",
    "SW": "Southwest",
    "WSW": "West-Southwest",
    "W": "West",
    "S": "South",
    "WNW": "West-Northwest",
    "NW": "Northwest",
    "NNW": "North-Northwest",
    "VARIABLE": "Fluctuate"
}

WEATHER_CODE = {
    "0":   ("Clear Skies", "https://www.bmkg.go.id/asset/img/icon-cuaca/cerah-{}.png"),
    "1":   ("Partly Cloudy", "https://www.bmkg.go.id/asset/img/icon-cuaca/cerah%20berawan-{}.png"),
    "2":   ("Partly Cloudy", "https://www.bmkg.go.id/asset/img/icon-cuaca/cerah%20berawan-{}.png"),
    "3":   ("Mostly Cloudy", "https://www.bmkg.go.id/asset/img/icon-cuaca/berawan-{}.png"),
    "4":   ("Overcast", "https://www.bmkg.go.id/asset/img/icon-cuaca/berawan%20tebal-{}.png"),
    "5":   ("Haze", "https://www.bmkg.go.id/asset/img/icon-cuaca/udara%20kabur-{}.png"),
    "10":  ("Smoke", "https://www.bmkg.go.id/asset/img/icon-cuaca/asap-{}.png"),
    "45":  ("Fog", "https://www.bmkg.go.id/asset/img/icon-cuaca/kabut-{}.png"),
    "60":  ("Light Rain", "https://www.bmkg.go.id/asset/img/icon-cuaca/hujan%20ringan-{}.png"),
    "61":  ("Rain", "https://www.bmkg.go.id/asset/img/icon-cuaca/hujan%20sedang-{}.png"),
    "63":  ("Heavy Rain", "https://www.bmkg.go.id/asset/img/icon-cuaca/hujan%20lebat-{}.png"),
    "80":  ("Isolated Shower", "https://www.bmkg.go.id/asset/img/icon-cuaca/hujan%20lokal-{}.png"),
    "95":  ("Severe Thunderstorm", "https://www.bmkg.go.id/asset/img/icon-cuaca/hujan%20petir-{}.png"),
    "97":  ("Severe Thunderstorm", "https://www.bmkg.go.id/asset/img/icon-cuaca/hujan%20petir-{}.png"),
    "100": ("Clear Skies", "https://www.bmkg.go.id/asset/img/icon-cuaca/cerah-{}.png"),
    "101": ("Partly Cloudy", "https://www.bmkg.go.id/asset/img/icon-cuaca/cerah%20berawan-{}.png"),
    "102": ("Partly Cloudy", "https://www.bmkg.go.id/asset/img/icon-cuaca/cerah%20berawan-{}.png"),
    "103": ("Mostly Cloudy", "https://www.bmkg.go.id/asset/img/icon-cuaca/berawan-{}.png"),
    "104": ("Overcast", "https://www.bmkg.go.id/asset/img/icon-cuaca/berawan%20tebal-{}.png")
}

PROVINCES = {
    "aceh": "DigitalForecast-Aceh.xml", 
    "bali": "DigitalForecast-Bali.xml", 
    "bangka_belitung": "DigitalForecast-BangkaBelitung.xml", 
    "banten": "DigitalForecast-Banten.xml", 
    "bengkulu": "DigitalForecast-Bengkulu.xml", 
    "dki_yogyakarta": "DigitalForecast-DIYogyakarta.xml", 
    "dki_jakarta": "DigitalForecast-DKIJakarta.xml", 
    "gorontalo": "DigitalForecast-Gorontalo.xml", 
    "jambi": "DigitalForecast-Jambi.xml", 
    "jawa_barat": "DigitalForecast-JawaBarat.xml", 
    "jawa_tengah": "DigitalForecast-JawaTengah.xml", 
    "jawa_Timur": "DigitalForecast-JawaTimur.xml", 
    "kalimantan_barat": "DigitalForecast-KalimantanBarat.xml", 
    "kalimantan_selatan": "DigitalForecast-KalimantanSelatan.xml", 
    "kalimantan_tengah": "DigitalForecast-KalimantanTengah.xml", 
    "kalimantan_timur": "DigitalForecast-KalimantanTimur.xml", 
    "kalimantan_utara": "DigitalForecast-KalimantanUtara.xml", 
    "kepulauan_riau": "DigitalForecast-KepulauanRiau.xml", 
    "lampung": "DigitalForecast-Lampung.xml", 
    "maluku": "DigitalForecast-Maluku.xml", 
    "maluku_utara": "DigitalForecast-MalukuUtara.xml", 
    "nusa_tenggara_barat": "DigitalForecast-NusaTenggaraBarat.xml", 
    "nusa_tenggara_timur": "DigitalForecast-NusaTenggaraTimur.xml", 
    "papua": "DigitalForecast-Papua.xml", 
    "papua_barat": "DigitalForecast-PapuaBarat.xml", 
    "riau": "DigitalForecast-Riau.xml", 
    "sulawesi_barat": "DigitalForecast-SulawesiBarat.xml", 
    "sulawesi_selatan": "DigitalForecast-SulawesiSelatan.xml", 
    "sulawesi_sengah": "DigitalForecast-SulawesiTengah.xml", 
    "sulawesi_tenggara": "DigitalForecast-SulawesiTenggara.xml", 
    "sulawesi_utara": "DigitalForecast-SulawesiUtara.xml", 
    "sumatera_barat": "DigitalForecast-SumateraBarat.xml", 
    "sumatera_selatan": "DigitalForecast-SumateraSelatan.xml", 
    "sumatera_utara": "DigitalForecast-SumateraUtara.xml", 
    "indonesia": "DigitalForecast-Indonesia.xml"
}