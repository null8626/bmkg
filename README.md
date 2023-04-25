# [bmkg][pypi-url] [![pypi][pypi-image]][pypi-url] [![downloads][downloads-image]][pypi-url] [![Build Status][ci-image]][ci-url] [![license][github-license-image]][github-license-url] [![BLAZINGLY FAST!!!][blazingly-fast-image]][blazingly-fast-url]

[pypi-image]: https://img.shields.io/pypi/v/bmkg.svg?style=flat-square
[pypi-url]: https://pypi.org/project/bmkg/
[downloads-image]: https://img.shields.io/pypi/dm/bmkg?style=flat-square
[ci-image]: https://github.com/null8626/bmkg/workflows/CI/badge.svg
[ci-url]: https://github.com/null8626/bmkg/actions/workflows/CI.yml
[github-license-image]: https://img.shields.io/github/license/null8626/bmkg?style=flat-square
[github-license-url]: https://github.com/null8626/bmkg/blob/main/LICENSE
[blazingly-fast-image]: https://img.shields.io/badge/speed-BLAZINGLY%20FAST!!!%20%F0%9F%94%A5%F0%9F%9A%80%F0%9F%92%AA%F0%9F%98%8E-brightgreen.svg?style=flat-square
[blazingly-fast-url]: https://twitter.com/acdlite/status/974390255393505280

Unofficial Python wrapper for the [BMKG (Meteorology, Climatology, and Geophysical Agency)](https://www.bmkg.go.id/) API.

## Installation

```console
$ pip install bmkg
```

## Examples

<details>
<summary><b>Fetching the weather of a specific province</b></summary>

```py
# import the module
import bmkg

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with bmkg.Client(unit=bmkg.IMPERIAL) as client:
    # fetch a weather forecast from a province
    weather = await client.get_forecast(bmkg.Province.JAKARTA)
    
    # get the weather forecast across various locations
    for forecast in weather.forecasts:
    
      # temperature of this forecast across various timeframes
      for temp in weather.temperature:
        print(f'temperature at {temp.date!r} is {temp.value!r}')

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
```

</details>
<details>
<summary><b>Fetching the latest earthquake</b></summary>

```py
# import the module
import bmkg

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with bmkg.Client(unit=bmkg.IMPERIAL) as client:
    # fetch the latest earthquake
    earthquake = await client.get_latest_earthquake()
    
    print(repr(earthquake))

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
```

</details>
<details>
<summary><b>Fetching the most recent earthquakes magnitude 5 or higher</b></summary>

```py
# import the module
import bmkg

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with bmkg.Client(unit=bmkg.IMPERIAL) as client:
    # fetch the most recent earthquakes magnitude 5 or higher
    earthquakes = await client.get_recent_earthquakes()
    
    # iterate through the generator
    for earthquake in earthquakes:
      print(repr(earthquake))

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
```

</details>
<details>
<summary><b>Fetching the most recent earthquakes regardless of their magnitude</b></summary>

```py
# import the module
import bmkg

import asyncio
import os

async def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with bmkg.Client(unit=bmkg.IMPERIAL) as client:
    # fetch the most recent earthquakes regardless of their magnitude
    earthquakes = await client.get_felt_earthquakes()
    
    # iterate through the generator
    for earthquake in earthquakes:
      print(repr(earthquake))

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
```

</details>