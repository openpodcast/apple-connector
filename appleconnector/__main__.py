"""
This module is used to run the library as a script.
"""

import os
import datetime as dt
import json

from loguru import logger

from .connector import AppleConnector


def main():
    """
    Run the appleconnector library as a script.
    """
    # To use the library as a script, fetch the config from the environment
    podcast_id = os.environ.get("PODCAST_ID")
    myacinfo = os.environ.get("MYACINFO")
    itctx = os.environ.get("ITCTX")

    connector = AppleConnector(
        podcast_id,
        myacinfo,
        itctx,
    )

    # Fetch metadata for podcast
    overview = connector.overview()
    logger.info("Podcast Overview= {}", json.dumps(overview, indent=4))

    # Fetch trends for all episodes
    end = dt.datetime.now()
    start = dt.datetime.now() - dt.timedelta(days=7)
    trends = connector.trends(start, end)
    logger.info("Trends= {}", json.dumps(trends, indent=4))

    # Fetch podcast episodes
    episodes = connector.episodes()
    logger.info("Podcast Episodes= {}", json.dumps(episodes, indent=4))

    # Fetch metadata for single podcast episode
    episode = connector.episode("1000581490950")
    logger.info("Podcast Episode= {}", json.dumps(episode, indent=4))


if __name__ == "__main__":
    main()
