#  Provides a python client for simply retrieving
#  and processing air quality data from the CHMI OpenData portal.
#  Copyright (C) 2025 chickendrop89

#  This library is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.

#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.

"""
Data constants for the library.
"""

from src import __version__

AQ_DATA_URL  = "https://opendata.chmi.cz/air_quality/now/data/airquality_1h_avg_CZ.csv"
METADATA_URL = "https://opendata.chmi.cz/air_quality/now/metadata/metadata.json"

USER_AGENT = f"python-czech-air-quality/{__version__}"
NOMINATIM_TIMEOUT = 10
REQUEST_TIMEOUT = 20

ETAG_URLS = {
    "aq_data_etag": AQ_DATA_URL,
    "metadata_etag": METADATA_URL
}

CACHE_FILE_NAME = "airquality_opendata_cache.json"
CACHE_METADATA_KEY = "__cache_metadata__"
TIMESTAMP_KEY = "timestamp"
ETAGS_KEY = "etags"

# Threshold for pollutant values considered as Error/N/A
CHMI_ERROR_THRESHOLD = 0

# Maximum number of nearby stations to search for fallback
MAX_FALLBACK_STATIONS = 5

EAQI_LEVELS = {
    0: "Error/N/A",
    25: "Good",
    50: "Fair",
    75: "Poor",
    100: "Very Poor",
}

EAQI_BANDS = {
    # Concentration breakpoints (µg/m³) and the corresponding AQI sub-index value
    # Format: (AQI_Value, Upper_Concentration_Limit)
    "PM10": [
        (20, 10), (35, 20), (50, 25), (70, 50), (100, 90),
        (150, 180), (200, 360), (300, 540), (500, 900)
    ],
    "PM2_5": [
        (20, 5), (35, 10), (50, 15), (70, 25), (100, 50),
        (150, 90),(200, 180), (300, 270), (500, 450)
    ],
    "O3": [
        (20, 60), (35, 100), (50, 140), (70, 180), (100, 240),
        (150, 300), (200, 400), (300, 500), (500, 600)
    ],
    "NO2": [
        (20, 40), (35, 100), (50, 200), (70, 400), (100, 700),
        (150, 1200), (200, 1700), (300, 2200), (500, 2700)
    ],
    "SO2": [
        (20, 50), (35, 100), (50, 200), (70, 350), (100, 500),
        (150, 750), (200, 1000), (300, 1300), (500, 1600)
    ],
}
