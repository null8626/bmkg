# [bmkg][pypi-url] [![pypi][pypi-image]][pypi-url] [![downloads][downloads-image]][pypi-url] [![github vulnerabilities][github-vulnerabilities-image]][github-url] [![languages][languages-image]][github-url] [![libraries.io dependents][libraries-io-dependents-image]][libraries-io-url] [![libraries.io score][libraries-io-score-image]][libraries-io-url] [![github code size][github-code-size-image]][github-url] [![license][github-license-image]][github-license-url] [![BLAZINGLY FAST!!!][blazingly-fast-image]][blazingly-fast-url]

[pypi-image]: https://img.shields.io/pypi/v/bmkg.svg?style=flat-square
[pypi-url]: https://pypi.org/project/bmkg/
[downloads-image]: https://img.shields.io/pypi/dm/bmkg?style=flat-square
[github-vulnerabilities-image]: https://img.shields.io/snyk/vulnerabilities/github/null8626/bmkg?style=flat-square
[languages-image]: https://img.shields.io/github/languages/top/null8626/bmkg?style=flat-square
[libraries-io-dependents-image]: https://img.shields.io/librariesio/dependents/pypi/bmkg?style=flat-square
[libraries-io-score-image]: https://img.shields.io/librariesio/sourcerank/pypi/bmkg?style=flat-square
[libraries-io-url]: https://libraries.io/pypi/bmkg
[github-url]: https://github.com/null8626/bmkg
[github-code-size-image]: https://img.shields.io/github/languages/code-size/null8626/bmkg?style=flat-square
[github-license-image]: https://img.shields.io/github/license/null8626/bmkg?style=flat-square
[github-license-url]: https://github.com/null8626/bmkg/blob/main/LICENSE
[blazingly-fast-image]: https://img.shields.io/badge/speed-BLAZINGLY%20FAST!!!%20%F0%9F%94%A5%F0%9F%9A%80%F0%9F%92%AA%F0%9F%98%8E-brightgreen.svg?style=flat-square
[blazingly-fast-url]: https://twitter.com/acdlite/status/974390255393505280

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