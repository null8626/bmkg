# bmkg
Unofficial Python wrapper for the BMKG (Meteorology, Climatology, and Geophysical Agency) API.<br>
Original API documentation: [https://data.bmkg.go.id/](https://data.bmkg.go.id/)<br>
Main official source: [https://www.bmkg.go.id/](https://www.bmkg.go.id/)<br>

## Installation
```bash
$ pip install bmkg
```

## Usage
```py
from bmkg import BMKG

# initiate the class
bmkg = BMKG()

# get indonesia's forecast
weather = await bmkg.get_forecast()
print(weather)

# get specific province's forecast
province_weather = await bmkg.get_forecast("aceh")
print(province_weather)

# get history of the latest earthquakes
earthquakes = await bmkg.get_recent_earthquakes()
for earthquake in earthquakes:
	print(earthquake)

# get wind forecast image
image = await bmkg.get_wind_forecast()
with open("wind-forecast.jpg", "wb") as f:
    f.write(image)
    f.close()

# close the class once done
await bmkg.close()
```