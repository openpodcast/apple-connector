import json
from loguru import logger
from .connector import AppleConnector
import os
import datetime as dt


def main():
    # To use the library as a script, fetch the config from the environment
    PODCAST_ID = os.environ.get("PODCAST_ID")
    MYACINFO = os.environ.get("MYACINFO")

    connector = AppleConnector(
        podcast_id=PODCAST_ID,
        myacinfo=MYACINFO,
    )

    # Fetch metadata for podcast
    # meta = connector.overview()
    # logger.info("Podcast Overview= {}", json.dumps(meta, indent=4))

    # Fetch podcast episodes
    # episodes = connector.episodes()
    # logger.info("Podcast Episodes= {}", json.dumps(episodes, indent=4))

    # Fetch metadata for single podcast episode
    episode = connector.episode("1000581490950")
    logger.info("Podcast Episode= {}", json.dumps(episode, indent=4))

if __name__ == "__main__":
    main()
