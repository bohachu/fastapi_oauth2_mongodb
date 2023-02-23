# setup.py
import yaml
from setuptools import setup, find_packages

yml = yaml.safe_load(open("package.yml"))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=yml["package_name"],
    version="0.0.5",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            f"mycommand={yml['package_name']}.__main__:main"
        ]
    }
)
