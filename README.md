# czech_air_quality
This library provides a python client for simply retrieving and processing air quality data from the CHMI `OpenData` portal, that provides data hourly.

It also contains the optional logic for automatically picking closest weather station to a location via `Nominatim`, automatically fetching multiple close stations to get measurements of all pollutants, caching, and a `EAQI` calculation

![PyPI - Version](https://img.shields.io/pypi/v/czech_air_quality?logo=python&logoColor=white) ![PyPI - Downloads](https://img.shields.io/pypi/dm/czech_air_quality?logo=python&logoColor=white) ![PyPI - Typing](https://img.shields.io/pypi/types/czech_air_quality?logo=python&logoColor=white)

---

## Installation
```bash
pip install czech_air_quality
```

**Requirements:**
- `Python` 3.10+
- `requests` >= 2.28.0
- `geopy` >= 2.3.0

---

## Quick Start
```python
from czech_air_quality import AirQuality

client = AirQuality()
aqi_level, description = client.get_air_quality_index("Prague")
print(f"AQI: {aqi_level} ({description})")
# Output: "AQI: 3 (Moderate)"
```

## API documentation
References/docs can be found below, this library also 
supports full typing hints:

https://czech-air-quality.readthedocs.io

## Data Source
Data from CHMI (Czech Hydrometeorological Institute) OpenData portal, updated hourly.

- Metadata: https://opendata.chmi.cz/air_quality/now/metadata/metadata.json
- Measurements: https://opendata.chmi.cz/air_quality/now/data/airquality_1h_avg_CZ.csv
