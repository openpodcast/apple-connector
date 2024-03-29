"""
This package allows you to fetch data from the inofficial Apple Podcast API.
The API is not documented and may change at any time. Use at your own risk.
"""

from .connector import AppleConnector
from .connector import Mode, SeriesMode, Metric, Dimension

__all__ = ["AppleConnector", "Mode", "SeriesMode", "Metric", "Dimension"]
