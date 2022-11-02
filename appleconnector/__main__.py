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
    meta = connector.overview()
    logger.info("Podcast Overview= {}", json.dumps(meta, indent=4))

    # # Fetch streams for podcast
    # end = dt.datetime.now()
    # start = dt.datetime.now() - dt.timedelta(days=7)
    # streams = connector.streams(start, end)
    # logger.info("Podcast Streams = {}", json.dumps(streams, indent=4))

    # # Fetch aggregate data for podcast
    # end = dt.datetime.now()
    # start = dt.datetime.now() - dt.timedelta(days=1)
    # aggregate = connector.aggregate(start, end)
    # logger.info("Podcast Aggregate = {}", json.dumps(aggregate, indent=4))

    # # Fetch podcast episodes
    # end = dt.datetime.now()
    # start = dt.datetime.now() - dt.timedelta(days=7)
    # # Get all episodes from iterator
    # for episode in connector.episodes(start, end):
    #     logger.info("Episode = {}", json.dumps(episode, indent=4))

    # # Fetch metadata for single podcast episode
    # episode_meta = connector.metadata(episode="48DAya24YOjS7Ez49JSH3y")
    # logger.info("Episode Streams = {}", json.dumps(episode_meta, indent=4))

    # # Fetch stream data for single podcast episode
    # end = dt.datetime.now()
    # start = dt.datetime.now() - dt.timedelta(days=7)
    # streams = connector.streams(start, end, episode="48DAya24YOjS7Ez49JSH3y")
    # logger.info("Episode Streams = {}", json.dumps(streams, indent=4))

    # # Fetch listener data for single podcast episode
    # end = dt.datetime.now()
    # start = dt.datetime.now() - dt.timedelta(days=7)
    # listeners = connector.listeners(start, end, episode="48DAya24YOjS7Ez49JSH3y")
    # logger.info("Episode Listeners = {}", json.dumps(listeners, indent=4))

    # # Fetch aggregate data for single podcast episode
    # end = dt.datetime.now()
    # start = dt.datetime.now() - dt.timedelta(days=7)
    # aggregate = connector.aggregate(start, end, episode="48DAya24YOjS7Ez49JSH3y")
    # logger.info("Episode Aggregate = {}", json.dumps(aggregate, indent=4))

    # # Fetch performance data for single podcast episode
    # performance = connector.performance("48DAya24YOjS7Ez49JSH3y")
    # logger.info("Episode Performance = {}", json.dumps(performance, indent=4))


if __name__ == "__main__":
    main()
