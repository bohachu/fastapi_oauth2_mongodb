# setup.py
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="fastapi_oauth2_mongodb",
    version="0.0.4",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mycommand=fastapi_oauth2_mongodb.__main__:main"
        ]
    }
)