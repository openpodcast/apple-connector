"""This module provides a class to connect to an unofficial Apple API
that provides podcast analytics. It relies on using cookies generated
manually by logging in with the appropriate user at https://podcastsconnect.apple.com.
"""

from enum import Enum
from typing import Dict, Optional
import datetime as dt
from time import sleep
from threading import RLock
from urllib.request import Request
from loguru import logger
import requests


# Podcast Base URL for API requests
BASE_URL = "https://podcastsconnect.apple.com/podcasts/pcc/v1/analytics"

# Initial delay between retries
DELAY_BASE = 2.0

# Maximum number of retries
MAX_RETRY_ATTEMPTS = 6

# This is the start date which is hardcoded in the Apple API
# It can be overridden by the user
DEFAULT_APPLE_START_DATE = dt.datetime(2017, 9, 19)


class Mode(str, Enum):
    """
    Enum for the different query duration modes available for the Apple
    Podcasts API.
    """

    ROLLING_60 = "ROLLING_60"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    ALL_TIME = "ALL_TIME"


class SeriesMode(str, Enum):
    """
    Enum for the different series modes available for the Apple
    Podcasts API.
    """

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class Metric(str, Enum):
    """
    Enum to represent a metric for the Apple Podcasts API.
    """

    LISTENERS = "LISTENERS"
    FOLLOWERS = "FOLLOWERS"
    TIME_LISTENED = "TIME_LISTENED"
    PLAYS = "PLAYS"


class Dimension(str, Enum):
    """
    Enum to represent a dimension for the Apple Podcasts API.
    """

    BY_CITY = "BY_CITY"
    BY_COUNTRY = "BY_COUNTRY"
    BY_EPISODES = "BY_EPISODES"
    BY_ENGAGEMENT = "BY_ENGAGEMENT"


class AppleConnector:
    """Representation of the inofficial Apple podcast API."""

    def __init__(
        self,
        podcast_id,
        myacinfo,
        itctx,
    ):
        """Initializes the AppleConnector object.

        Args:
            podcast_id (str, optional): Apple Podcast ID.
            myacinfo (str): Apple cookie.
            itctx (str): Apple cookie.
        """

        self.base_url = BASE_URL
        self.podcast_id = podcast_id
        self.myacinfo = myacinfo
        self.itctx = itctx
        self.default_params = {
            "showId": self.podcast_id,
        }

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}/{path}"

    def _request(
        self, endpoint: str, *, params: Optional[Dict[str, str]] = None
    ) -> dict:
        url = self._build_url(endpoint)
        logger.trace("url = {}", url)
        delay = DELAY_BASE

        # Merge default params with provided params
        if params is None:
            params = {}
        params = {**self.default_params, **params}

        for attempt in range(MAX_RETRY_ATTEMPTS):

            # Create request object with requests and trace it before sending
            request = requests.Request(
                "GET",
                url,
                params=params,
                headers={
                    "Accept": "application/json, text/plain, */*",
                },
                cookies={
                    "myacinfo": self.myacinfo,
                    "itctx": self.itctx,
                },
            )
            prepared_request = request.prepare()
            logger.trace("request - {}", prepared_request.url)
            response = requests.Session().send(prepared_request)

            if response.status_code in (429, 502, 503, 504):
                delay *= 2
                logger.log(
                    ("INFO" if attempt < 3 else "WARNING"),
                    'Got {} for URL "{}", next delay: {}s',
                    response.status_code,
                    url,
                    delay,
                )
                sleep(delay)
                continue

            if not response.ok:
                logger.error("Error in API:" + endpoint)
                logger.info(response.request.url)
                logger.info(response.request.body)
                logger.info(response.request.headers)
                logger.info(response.status_code)
                logger.info(response.headers)
                logger.info(response.text)
                response.raise_for_status()

            logger.trace("response = {}", response.text)
            return response.json()

        raise Exception("All retries failed!")

    def overview(
        self,
        start: dt.date = DEFAULT_APPLE_START_DATE,
        end: dt.date = dt.date.today(),
        mode: Mode = Mode.ALL_TIME,
        series_mode: SeriesMode = SeriesMode.MONTHLY,
    ) -> dict:
        """Loads overview data for podcast.

        Args:
            None

        Returns:
            dict: Response data from API.
        """

        params = {
            # Hardcoded start date taken from Apple Podcast Connect
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "mode": mode.value,
            "seriesMode": series_mode.value,
        }
        return self._request("showOverviewV3", params=params)

    def episodes(
        self,
        date: dt.date = DEFAULT_APPLE_START_DATE,
        mode: Mode = Mode.ALL_TIME,
    ) -> dict:
        """Loads episode data for podcast.

        Args:
            None

        Returns:
            dict: Response data from API.
        """

        params = {
            # Note that it's not called 'start' but 'date'.
            # Switching between both param names seems to be a quirk of the API.
            "date": date.strftime("%Y-%m-%d"),
            "mode": mode.value,
        }
        return self._request("episodes", params=params)

    def episode(
        self,
        episode_id: str,
        start: dt.date = DEFAULT_APPLE_START_DATE,
        end: dt.date = dt.date.today(),
        mode: Mode = Mode.ALL_TIME,
    ) -> dict:
        """Episode details endpoint

        Args:
            episode_id (str): Apple Podcast Episode ID.

        Returns:
            dict: Response data from API.
        """

        params = {
            # Yet another way to specify the date range. o_O
            "startDate": start.strftime("%Y-%m-%d"),
            "endDate": end.strftime("%Y-%m-%d"),
            "mode": mode.value,
            "episodeId": episode_id,
        }
        return self._request("episodeDetails", params=params)

    def trends(
        self,
        start: dt.date = DEFAULT_APPLE_START_DATE,
        end: dt.date = dt.date.today(),
        mode: Mode = Mode.ALL_TIME,
        series_mode: SeriesMode = SeriesMode.DAILY,
        metric: Metric = Metric.PLAYS,
        dimension: Dimension = Dimension.BY_COUNTRY,
    ) -> dict:
        """Loads trend data for podcast.

        Daily metrics, 16 dimensions which can be even broke down further,
        (e.g. episode listens in Germany by engaged users)

        Args:
            start (dt.date): Start date.
            end (dt.date): End date.

        Returns:
            dict: Response data from API.
        """

        params = {
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "seriesMode": series_mode.value,
            "metric": metric.value,
            "dimension": dimension.value,
            "mode": mode.value,
        }
        return self._request("showTrendsV2", params=params)
