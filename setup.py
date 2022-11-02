from setuptools import find_packages, setup

setup(
    name='appleconnector',
    packages=find_packages(include=['appleconnector']),
    version='0.1.0',
    description='Apple Connector for Podcast Data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Open Podcast',
    license='MIT',
    entry_points={
        'console_scripts': [
            'appleconnector = appleconnector.__main__:main',
        ]
    },
    install_requires=[
        'requests',
        'loguru',
        'PyYAML',
        'tenacity'
    ],
)
