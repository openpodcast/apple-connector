"""This module provides a class to connect to an unofficial Apple API
that provides podcast analytics. It relies on using cookies generated
manually by logging in with the appropriate user at https://podcastsconnect.apple.com.
"""

from typing import Dict, Optional
import datetime as dt
from time import sleep
from threading import RLock
from urllib.request import Request
from loguru import logger
import random
import string
import base64
import hashlib
import re
import json

import requests
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential
import yaml


BASE_URL = "https://podcastsconnect.apple.com/podcasts/pcc/v1/analytics"
DELAY_BASE = 2.0


def random_string(
    length: int,
    chars: str = string.ascii_lowercase + string.ascii_uppercase + string.digits,
) -> str:
    """Simple helper function to generate random strings suitable for use with Apple"""
    return "".join(random.choices(chars, k=length))


class AppleConnector:
    """Representation of the inofficial Apple podcast API."""

    def __init__(
        self,
        podcast_id,
        myacinfo,
    ):
        """Initializes the AppleConnector object.

        Args:
            podcast_id (str, optional): Apple Podcast ID.
            myacinfo (str, optional): Apple cookie.
        """

        self.base_url = BASE_URL
        self.podcast_id = podcast_id
        self.myacinfo = myacinfo
        self.default_params = {
            "showId": self.podcast_id,
        }

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}/{path}"

    def _request(self, endpoint: str, *, params: Optional[Dict[str, str]] = None) -> dict:
        url = self._build_url(endpoint)
        logger.trace("url = {}", url)
        delay = DELAY_BASE

        # Merge default params with provided params
        if params is None:
            params = {}
        params = {**self.default_params, **params}

        for attempt in range(6):
            sleep(delay)

            # Create request object with requests and trace it before sending
            request = requests.Request(
                "GET",
                url,
                params=params,
                headers={
                    'Accept': 'application/json, text/plain, */*',
                },
                cookies = {
                    'myacinfo': self.myacinfo
                }
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
                continue

            if not response.ok:
                logger.error("Error in API:")
                logger.info(response.status_code)
                logger.info(response.headers)
                logger.info(response.text)
                response.raise_for_status()

            logger.trace("response = {}", response.text)
            return response.json()

        raise Exception("All retries failed!")

    def overview(self) -> dict:
        """Loads overview data for podcast.

        Args:
            None

        Returns:
            dict: Response data from API.
        """

        params = {
            # Hardcoded start date taken from Apple Podcast Connect
            'start': '2017-09-19',
            'end': dt.datetime.now().strftime("%Y-%m-%d"),
            'mode': 'ALL_TIME',
            'seriesMode': 'MONTHLY',
        }
        return self._request("showOverviewV3", params=params)

    def episodes(self) -> dict:
        """Loads episode data for podcast.

        Args:
            None

        Returns:
            dict: Response data from API.
        """

        params = {
            # Hardcoded date taken from Apple Podcast Connect.
            # Note that it's not called 'start' but 'date'.
            # Switching between both params seems to be a quirk of the API.
            'date': '2017-09-19',
            'mode': 'ALL_TIME',
        }
        return self._request("episodes", params=params)

    def episode(self, episode_id: str) -> dict:
        """Episode details endpoint

        Args:
            episode_id (str): Apple Podcast Episode ID.

        Returns:
            dict: Response data from API.
        """

        params = {
            # Yet another way to specify the date range. o_O
            'startDate': '2017-09-19',
            'endDate': dt.datetime.now().strftime("%Y-%m-%d"),
            'mode': 'ALL_TIME',
            'episodeId': episode_id,
        }
        return self._request("episodeDetails", params=params)

    def trends(self, start: dt.date, end: dt.date) -> dict:
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
            'start': start.strftime("%Y-%m-%d"),
            'end': end.strftime("%Y-%m-%d"),
            'seriesMode': 'DAILY',
            'metric': 'PLAYS',
            'dimension': 'BY_EPISODES',
            'mode': 'WEEKLY',
        }
        return self._request("showTrendsV2", params=params)
