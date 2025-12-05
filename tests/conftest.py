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
Pytest configuration and shared fixtures for tests.
"""

from unittest.mock import Mock, patch
from datetime import datetime, timezone
import tempfile
import pytest

@pytest.fixture
def mock_data_manager():
    """Provide a mock DataManager instance."""
    with patch("src.data_manager.DataManager") as mock_dm:
        instance = Mock()
        instance.raw_data_json = None
        instance.actualized_time = datetime.now(timezone.utc)
        instance.is_data_fresh.return_value = True
        instance.ensure_latest_data = Mock()

        mock_dm.return_value = instance
        yield instance


@pytest.fixture
def mock_stations():
    """Provide realistic mock station data."""
    return [
        {
            "Name": "Prague - Vinohrady",
            "LocalityCode": "1",
            "Region": "Prague",
            "Latitude": 50.0755,
            "Longitude": 14.4378,
            "IdRegistrations": ["1001", "1002"],
        },
        {
            "Name": "Brno",
            "LocalityCode": "2",
            "Region": "South Moravia",
            "Latitude": 49.1951,
            "Longitude": 16.6068,
            "IdRegistrations": ["2001", "2002"],
        },
        {
            "Name": "Ostrava",
            "LocalityCode": "3",
            "Region": "Moravia-Silesia",
            "Latitude": 49.8209,
            "Longitude": 18.2625,
            "IdRegistrations": ["3001", "3002"],
        },
    ]


@pytest.fixture
def mock_measurements():
    """Provide realistic mock measurement data."""
    return {
        "1001": {
            "ComponentCode": "PM10",
            "ComponentName": "Particulate matter < 10 µm",
            "Unit": "µg/m³",
            "value": "25.5",
        },
        "1002": {
            "ComponentCode": "O3",
            "ComponentName": "Ozone",
            "Unit": "µg/m³",
            "value": "75.0",
        },
        "2001": {
            "ComponentCode": "PM10",
            "ComponentName": "Particulate matter < 10 µm",
            "Unit": "µg/m³",
            "value": "30.2",
        },
        "2002": {
            "ComponentCode": "NO2",
            "ComponentName": "Nitrogen dioxide",
            "Unit": "µg/m³",
            "value": "45.8",
        },
        "3001": {
            "ComponentCode": "PM2_5",
            "ComponentName": "Fine particulate matter",
            "Unit": "µg/m³",
            "value": "15.3",
        },
        "3002": {
            "ComponentCode": "SO2",
            "ComponentName": "Sulfur dioxide",
            "Unit": "µg/m³",
            "value": "5.0",
        },
    }


@pytest.fixture
def mock_metadata():
    """Provide realistic mock metadata structure."""
    return {
        "Localities": [
            {
                "Name": "Prague - Vinohrady",
                "LocalityCode": "1",
                "Region": "Prague",
                "Latitude": 50.0755,
                "Longitude": 14.4378,
                "IdRegistrations": ["1001", "1002"],
                "MeasuringPrograms": [],
            },
            {
                "Name": "Brno",
                "LocalityCode": "2",
                "Region": "South Moravia",
                "Latitude": 49.1951,
                "Longitude": 16.6068,
                "IdRegistrations": ["2001", "2002"],
                "MeasuringPrograms": [],
            },
        ],
        "id_registration_to_component": {
            "1001": {
                "ComponentCode": "PM10",
                "ComponentName": "Particulate matter < 10 µm",
                "Unit": "µg/m³",
            },
            "1002": {"ComponentCode": "O3", "ComponentName": "Ozone", "Unit": "µg/m³"},
            "2001": {
                "ComponentCode": "PM10",
                "ComponentName": "Particulate matter < 10 µm",
                "Unit": "µg/m³",
            },
            "2002": {
                "ComponentCode": "NO2",
                "ComponentName": "Nitrogen dioxide",
                "Unit": "µg/m³",
            },
        },
    }


@pytest.fixture
def temp_cache_dir():
    """Provide a temporary directory for cache files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def pytest_configure(config):
    """Configure pytest options."""
    config.addinivalue_line("testpaths", "tests")


def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
