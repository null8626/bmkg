# bmkg
Python wrapper for the BMKG (Meteorology, Climatology, and Geophysical Agency) API.
Original API documentation: [https://data.bmkg.go.id/](https://data.bmkg.go.id/)
Main official source: [https://www.bmkg.go.id/](https://www.bmkg.go.id/)

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

# get wind forecast image
image = await bmkg.get_wind_forecast()
with open("wind-forecast.jpg", "wb") as f:
    f.write(image)
    f.close()

# close the class once done
await bmkg.close()
```