from setuptools import setup, find_packages

from compgen import __version__

setup(
    name="compgen",
    version=__version__,
    packages=find_packages(
        include=["compgen/*"]
    ),
    install_requires=[
        "pydantic==2.5.0"
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0"
        ]
    }
)