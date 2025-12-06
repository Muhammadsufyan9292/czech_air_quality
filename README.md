# czech_air_quality
This library provides a python client for simply retrieving and processing air quality data from the CHMI `OpenData` portal, that provides data hourly.

It also contains the optional logic for automatically picking closest weather station to a location via `Nominatim`, automatically fetching multiple close stations to get measurements of all pollutants, caching, and a `EAQI` calculation

![PyPI - Version](https://img.shields.io/pypi/v/czech_air_quality?logo=python&logoColor=white) ![PyPI - Downloads](https://img.shields.io/pypi/dm/czech_air_quality?logo=python&logoColor=white) ![PyPI - Typing](https://img.shields.io/pypi/types/czech_air_quality?logo=python&logoColor=white)

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Public Methods](#public-methods)
4. [Exception Classes](#exception-classes)
5. [Data Structures](#data-structures)
6. [Examples](#examples)
7. [Configuration](#configuration)

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
aqi = client.get_air_quality_index("Prague")
print("AQI level:", aqi)
# Output: "AQI level: 3"
```

---

## Public Methods
### Class Methods

#### `get_all_station_names()`
Get all known air quality station names without initializing a full client.

```python
@classmethod
def get_all_station_names() -> list[str | None]
```

**Returns:**
- `list[str | None]` - List of station names, or empty list if unavailable

**Example:**
```python
stations = AirQuality.get_all_station_names()
print("Total stations:", len(stations))
print("First 5 stations:")
for station in stations[:5]:
    print("-", station)

# Output:
# Total stations: 41
# First 5 stations:
# - Ostrava-Fifejdy
# - Frýdek-Místek
# - Beroun
# - Třinec-Kosmos
# - Bělotín
```

---

### Instance Properties
#### `actualized_time`
Timestamp when the data was last updated by the `CHMI` source.

```python
@property
def actualized_time() -> datetime
```

**Returns:**
- `datetime` - UTC timestamp of the most recent data update

**Example:**
```python
client = AirQuality()
print("Data last updated:", client.actualized_time)
# Output: Data last updated: 2025-11-16 21:37:37.612407+00:00
```

#### `is_data_fresh`
Check if cached data is still valid via ETag validation.
```python
@property
def is_data_fresh() -> bool
```

**Returns:**
- `bool` - `True` if cached data is current; `False` if needs refresh

**Example:**
```python
client = AirQuality()
if client.is_data_fresh:
    print("Using cached data")
else:
    print("Cache is stale")
```

---

### Instance Methods
#### `find_nearest_station(city_name)`
Find the air quality station nearest to a specified city.

```python
def find_nearest_station(city_name: str) -> tuple[dict, float]
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `city_name` | `str` | Name of the city to search for |

**Returns:**
- `tuple[dict, float]` - Station metadata dict and distance in kilometers

**Raises:**
- `StationNotFoundError` - If the city or nearby stations cannot be found

**Example:**
```python
client = AirQuality()
station, distance = client.find_nearest_station("Prague")

print("Nearest station:", station["Name"])
print("Distance:", distance, "km")

# Output:
# Nearest station: Praha 1-n. Republiky
# Distance: 0.45 km
```

#### `get_air_quality_index(city_name)`
Get the overall EAQI for the nearest station to a city.

```python
def get_air_quality_index(city_name: str) -> int
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `city_name` | `str` | Name of the city |

**Returns:**
- `int` - EAQI level (0-6)

**Details:**
- Returns the highest sub-index across all measured pollutants
- Supports PM10, PM2.5, O3, NO2, SO2

**EAQI Scale (0-6):**
| Level | Description |
|-------|-------------|
| 0 | Error/N/A |
| 1 | Good |
| 2 | Fair |
| 3 | Moderate |
| 4 | Poor |
| 5 | Very Poor |
| 6 | Extremely Poor |

**Example:**
```python
aqi = client.get_air_quality_index("Ostrava")
print("Air Quality Index for Ostrava:", aqi)

if aqi == 1:
    status = "Good"
elif aqi == 2:
    status = "Fair"
# ...etc
else:
    status = "Error/No data"

print("Status:", status)

# Output:
# Air Quality Index for Ostrava: 2
# Status: Fair
```

#### `get_air_quality_report(city_name)`
Get a comprehensive air quality report for the nearest station.

```python
def get_air_quality_report(city_name: str) -> dict
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `city_name` | `str` | Name of the city |

**Returns:**
- `dict` - Comprehensive report dictionary (see [Air Quality Report](#air-quality-report))

**Example:**
```python
report = client.get_air_quality_report("Brno")

if "Error" in report:
    print("Error:", report["Error"])
else:
    print("Station:", report["station_name"])
    print("Region:", report["region"])
    print("Distance:", report["distance_km"], "km")
    print("Overall AQI:", report["air_quality_index_code"])
    print("Status:", report["air_quality_index_description"])
    
    print("\nTop pollutants:")
    for meas in report["measurements"]:
        if meas["sub_aqi"] > 0:
            print("-", meas["pollutant_code"] + ":", meas["formatted_measurement"])

# Station: Brno-Dětská nemocnice
# Region: Jihomoravský
# Distance: 0.00 km
# Overall AQI: 4
# Status: Poor
# 
# Top pollutants:
# - PM10: 48 µg/m³
# - O3: 35 ppb
# ...
```

#### `get_pollutant_measurement(city_name, pollutant_code)`
Get detailed measurement data for a specific pollutant at the nearest station.

```python
def get_pollutant_measurement(city_name: str, pollutant_code: str) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `city_name` | `str` | Name of the city |
| `pollutant_code` | `str` | Pollutant code (e.g., `"PM10"`, `"NO2"`) - case insensitive |

**Returns:**
- `dict` - Measurement dictionary (see [Pollutant Measurement](#pollutant-measurement))

**Raises:**
- `StationNotFoundError` - If station not found
- `PollutantNotReportedError` - If none of the 5 nearest stations measure this pollutant

**Example:**
```python
try:
    measurement = client.get_pollutant_measurement("Ostrava", "PM10")
    print("City:", measurement["city_searched"])
    print("Station:", measurement["station_name"])
    print("Pollutant:", measurement["pollutant_code"])
    print("Value:", measurement["formatted_measurement"])
    print("Status:", measurement["measurement_status"])
except PollutantNotReportedError as e:
    print("Error:", e)

# City: Ostrava
# Station: Ostrava-Fifejdy
# Pollutant: PM10
# Value: 52 µg/m³
# Status: Measured
```

#### `force_fetch_fresh()`
Force fetching fresh data from the source without waiting for the internal cache timer to expire.

```python
def force_fetch_fresh() -> None
```

**Behavior:**
- Bypasses the normal 20-minute cache timeout
- Still uses cached data if server returns 304 (Not Modified) via ETag
- Raises `DataDownloadError` if download fails and no cache is available

**Example:**
```python
print("Using potentially cached data")
report1 = client.get_air_quality_report("Prague")

# Force a refresh from server
client.force_fetch_fresh()
print("Using fresh data")
report2 = client.get_air_quality_report("Prague")
```

---

## Exception Classes
### DataDownloadError
Raised when data cannot be downloaded or is invalid.

```python
class DataDownloadError(AirQualityError):
    """Raised when data cannot be downloaded or is invalid."""
```

**Common Causes:**
- Network connectivity issues
- Server returned invalid `JSON` or `CSV`
- `HTTP` error or timeout during download

### StationNotFoundError
Raised when a city or station cannot be found.

```python
class StationNotFoundError(AirQualityError):
    """Raised when a city or station cannot be found."""
```

**Common Causes:**
- The city name is not in the czech region
- Geocoding service unavailable

### PollutantNotReportedError
Raised when a station doesn't report data for a requested pollutant.

```python
class PollutantNotReportedError(AirQualityError):
    """Raised when station doesn't report this pollutant."""
```

**Common Causes:**
- When using `get_pollutant_measurement()`
    - If `use_nominatim=True` and all `neighbour_station_limit=20` stations near a city don't report the requested pollutant
    - If `use_nominatim=False` and an exact station doesn't report requested pollutant

### CacheError
Raised when there is an error related to caching data.

```python
class CacheError(AirQualityError):
    """Raised when there is an error related to caching data."""
```

**Common Causes:**
- Operating system errors
- Cache file is corrupted or unreadable

**Example:**
```python
from czech_air_quality import (
    AirQuality,
    StationNotFoundError,
    PollutantNotReportedError,
    DataDownloadError
)

try:
    client = AirQuality()
    measurement = client.get_pollutant_measurement("Unknown City", "PM10")
except StationNotFoundError as e:
    print("Station error:", e)
except PollutantNotReportedError as e:
    print("Pollutant error:", e)
except DataDownloadError as e:
    print("Download error:", e)

# Output: "Pollutant error: ..."
```

---

## Data Structures
### Air Quality Report
Dictionary returned by `get_air_quality_report()`:

```python
{
    "city_searched": str,                    # Original search term
    "station_name": str,                     # Nearest station name
    "station_code": str,                     # Station locality code
    "region": str,                           # Czech region name
    "distance_km": str,                      # Distance as "X.XX"
    "air_quality_index_code": int,           # EAQI level (0-6)
    "air_quality_index_description": str,    # Description (e.g., "Good")
    "actualized_time_utc": str,              # ISO format UTC timestamp
    "measurements": list[dict],              # List of measurements
    
    # Error response:
    "Error": str                             # Error message
}
```

### Measurement Object (from report)
Individual pollutant measurement:

```python
{
    "pollutant_code": str,                   # Code (e.g., "PM10")
    "pollutant_name": str,                   # Full name
    "unit": str,                             # Unit (e.g., "µg/m³")
    "value": float | None,                   # Numeric value
    "sub_aqi": int,                          # Sub-index (-1 if invalid)
    "formatted_measurement": str             # Display string
}
```

### Pollutant Measurement
Dictionary returned by `get_pollutant_measurement()`:

```python
{
    "city_searched": str,                    # Original search term
    "station_name": str,                     # Station name
    "pollutant_code": str,                   # Pollutant code (uppercase)
    "pollutant_name": str,                   # Full name
    "unit": str,                             # Measurement unit
    "value": float | None,                   # Numeric value
    "measurement_status": str,               # Status string
    "formatted_measurement": str             # Display string
}
```

---

## Examples
### Example 1: Basic Setup

```python
from czech_air_quality import AirQuality

client = AirQuality()
print("Data fresh:", client.is_data_fresh)
print("Last update:", client.actualized_time)
```

### Example 2: Find Nearest Station
```python
client = AirQuality()

station, distance = client.find_nearest_station("Brno")
print("Station:", station["Name"])
print("Region:", station["Region"])
print("Distance:", distance, "km")
```

### Example 3: Get Air Quality Index
```python
aqi = client.get_air_quality_index("Prague")
print("AQI:", aqi)

if aqi == 1:
    status = "Good"
elif aqi == 2:
    status = "Fair"
elif aqi == 3:
    status = "Moderate"
elif aqi == 4:
    status = "Poor"
elif aqi == 5:
    status = "Very Poor"
elif aqi == 6:
    status = "Extremely Poor"
else:
    status = "Error/No data"

print("AQI description:", status)
```

### Example 4: Get Full Report
```python
report = client.get_air_quality_report("Ostrava")

print("Station:", report["station_name"])
print("Overall AQI:", report["air_quality_index_code"])

for measurement in report["measurements"]:
    code = measurement["pollutant_code"]
    value = measurement["formatted_measurement"]
    print(code + ":", value)
```

### Example 5: Single Pollutant
```python
pm10 = client.get_pollutant_measurement("Ostrava", "PM10")

print("City:", pm10["city_searched"])
print("Pollutant:", pm10["pollutant_name"])
print("Value:", pm10["formatted_measurement"])
print("Status:", pm10["measurement_status"])
```

### Example 6: List Stations
```python
stations = AirQuality.get_all_station_names()

print("Total stations:", len(stations))
for station in stations:
    print("-", station)
```

### Example 7: Filter by Region
```python
client = AirQuality(region_filter="Moravskoslezský")

stations = client.all_stations
print("Stations in region:", len(stations))

for station in stations:
    print("-", station["Name"])
```

### Example 8: Using Exact Station Names (No Nominatim)
```python
client = AirQuality(use_nominatim=False)
report = client.get_air_quality_report("Ostrava-Fifejdy")
print(f"AQI: {report['air_quality_index_code']}")
```

**Note:** This approach requires knowing exact station names.
Use `get_all_station_names()` to list all available stations.

### Example 9: Error Handling
```python
from czech_air_quality import AirQuality, StationNotFoundError

try:
    report = client.get_air_quality_report("Unknown")
except StationNotFoundError:
    print("City not found")
```

---

## Configuration
### Logging
Logging of the library debugging details
```python
import logging
logging.getLogger("czech_air_quality").setLevel(logging.DEBUG)
```

### Timeouts
Adjust HTTP and geocoding timeouts:
```python
client = AirQuality(
    request_timeout=30,
    nominatim_timeout=15
)
```

### Caching
Control caching behavior:
```python
# Use cache (default)
client = AirQuality(disable_caching=False)

# Disable cache for fresh data
client = AirQuality(disable_caching=True)

# Check cache status
print("Fresh:", client.is_data_fresh)

# Force fresh data before 20-minute TTL expires
client.force_fetch_fresh()
```

**Caching Strategy:**
The library implements a freshness check:
1. **Cache Hit (Recent):** If cached data is < 20 minutes old, use it immediately
2. **ETag Validation:** If cache is > 20 minutes old, perform HTTP-HEAD request with ETag
   - If server returns **304 (Not Modified)**, trust cache for another 20 minutes
   - If server returns **200 (Modified)**, download full data
3. **Network Error:** If network unavailable but cache exists, use stale cache with warning
4. **Force Refresh:** `force_fetch_fresh()` bypasses age check but respects ETags

### Nominatim Geocoding
Control whether to use Nominatim for city name lookups:

```python
# Enable Nominatim (default) - looks up city coordinates
client = AirQuality(use_nominatim=True)
report = client.get_air_quality_report("Prague")

# Disable Nominatim - only exact station name matches
client = AirQuality(use_nominatim=False)
report = client.get_air_quality_report("Praha 1-n. Republiky")
```

**Behavior:**
- `use_nominatim=True` (default): Accepts city names, geocodes them to coordinates, finds nearest station
- `use_nominatim=False`: Only accepts exact station names from the network; no geocoding needed

### Region Filtering
Limit results to specific regions:
```python
regions = [
    "Jihomoravský",
    "Jihočeský",
    "Karlovarský",
    "Královéhradecký",
    "Liberecký",
    "Moravskoslezský",
    "Olomoucký",
    "Pardubický",
    "Plzeňský",
    "Praha",
    "Středočeský",
    "Ústecký",
    "Vysočina",
    "Zlínský"
]

client = AirQuality(region_filter="jihomoravský")
```

---

## Data Source
Data from CHMI (Czech Hydrometeorological Institute) OpenData portal, updated hourly.

- Metadata: https://opendata.chmi.cz/air_quality/now/metadata/metadata.json
- Measurements: https://opendata.chmi.cz/air_quality/now/data/airquality_1h_avg_CZ.csv
