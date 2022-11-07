import pytest
import json
from .connector import Metric, Dimension, Mode, SeriesMode


def test_serialize():
    """
    Enum fields are JSON-serializable (required by requests)
    """
    for variant in [
        Metric.LISTENERS,
        Dimension.BY_CITY,
        Mode.MONTHLY,
        SeriesMode.WEEKLY,
    ]:
        json.dumps(variant)
