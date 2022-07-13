# bmkg
Unofficial Python wrapper for the [BMKG (Meteorology, Climatology, and Geophysical Agency)](https://www.bmkg.go.id/) API.<br>

## Installation
```bash
$ pip install bmkg
```

## Importing
```py
from bmkg import BMKG
```

## Usage
P.S: wrap this example in an async function!
```py
from bmkg import Province

# initiate the class
bmkg = BMKG()

forecast = await bmkg.get_forecast(Province.jawa_barat)
print(forecast)

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