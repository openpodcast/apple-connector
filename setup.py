"""
Apple Connector for Podcast Data

This package allows you to fetch data from the inofficial Apple Podcast API.
The API is not documented and may change at any time. Use at your own risk.
"""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="appleconnector",
    packages=find_packages(include=["appleconnector"]),
    version="0.4.0",
    description="Apple Connector for Podcast Data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Open Podcast",
    license="MIT",
    entry_points={
        "console_scripts": [
            "appleconnector = appleconnector.__main__:main",
        ]
    },
    install_requires=["requests", "loguru", "PyYAML", "tenacity"],
)
