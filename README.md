# Apple Connector

[![Docs](https://readthedocs.org/projects/apple-connector/badge?version=latest)](https://apple-connector.readthedocs.io)

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

We use [Pipenv] for virtualenv and dev dependency management. With Pipenv
installed:

1. Install your locally checked out code in [development mode], including its
   dependencies, and all dev dependencies into a virtual environment:

```sh
pipenv sync --dev
```

2. Create an environment file and fill in the required values:

```sh
cp .env.example .env
```

3. Run the script in the virtual environment, which will [automatically load
   your `.env`][env]:

```sh
pipenv run appleconnector
```

To add a new dependency for use during the development of this library:

```sh
pipenv install --dev $package
```

To add a new dependency necessary for the correct operation of this library, add
the package to the `install_requires` section of `./setup.py`, then:

```sh
pipenv install
```

To publish the package:

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```

or

```sh
make publish
```
