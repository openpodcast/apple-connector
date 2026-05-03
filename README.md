# Apple Connector

[![Docs](https://readthedocs.org/projects/apple-connector/badge?version=latest)](https://apple-connector.readthedocs.io)

[![OpenPodcast Banner](https://raw.githubusercontent.com/openpodcast/banner/main/openpodcast-banner.png)](https://openpodcast.app/)

This is a simple library for connecting to the inofficial Apple podcast API.  
It can be used to export data from your dashboard at
https://podcastsconnect.apple.com.

## Supported Data

- Podcast Overview
- Trends
- Episodes Overview
- Episode Details

## Credentials

We need the `myacinfo` and `itctx` cookies from your browser to authenticate.
They can be found through the network tab in your browser's developer tools.
Add them to `.env` as `MYACINFO` and `ITCTX`.
(You need to quote the values, as they may contain `|`.)

## Installation

```
pip install appleconnector
```

## Usage as a library

```python
from appleconnector import AppleConnector

# Set up the connector
connector = AppleConnector(
    podcast_id='1642486726',
    myacinfo="your_myacinfo_cookie",
    itctx="your_itctx_cookie"
)

# Get Podcast overview data
connector.overview()

# ...
```

See `__main.py__` for all endpoints.

## Development

We use [uv](https://docs.astral.sh/uv/) for virtualenv and dependency
management. With uv installed:

1. Install your locally checked out code, including its dependencies and all
   dev dependencies, into a virtual environment:

```sh
uv sync --all-extras --dev
```

2. Create an environment file and fill in the required values:

```sh
cp .env.example .env
```

3. Run the script in the virtual environment:

```sh
uv run appleconnector
```

To add a new dev dependency:

```sh
uv add --dev $package
```

To add a new runtime dependency:

```sh
uv add $package
```

### Releasing

Releases are published to PyPI automatically by CI when a GitHub release is
created. To cut a new release:

1. Bump the `version` field in `pyproject.toml`.
2. Commit and push to `main`.
3. Create a GitHub release with a matching `vX.Y.Z` tag — the `deploy` job
   will run `uv build` and upload the artifacts to PyPI.

To build the package locally:

```sh
uv build
```
