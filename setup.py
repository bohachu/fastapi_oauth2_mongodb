from setuptools import setup, find_packages

setup(
    name="fastapi_oauth2_mongodb",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pymongo",
        "uvicorn",
        "passlib",
        "pydantic",
        "python-jose[cryptography]",
        "python-multipart",
        "bcrypt"
    ],
    entry_points={
        "console_scripts": [
            "mycommand=fastapi_oauth2_mongodb.__main__:main"
        ]
    }
)
