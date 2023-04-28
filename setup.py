#!/usr/bin/env python3

# Copyright 2023 Facundo Batista
# Licensed under the GPL v3 License
# For further info, check https://github.com/facundobatista/foffinf

"""Setup script for foffinf."""

from setuptools import setup


setup(
    name="foffinf",
    version="0.1",
    author="Facundo Batista",
    author_email="facundo@taniquetil.com.ar",
    description="A way to use stdlib's logging with the new Format Specification Mini-Language.",
    long_description=open("README.md", "rt", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/facundobatista/foffinf",
    license="GPL-v3",
    packages=["foffinf"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[],
    python_requires=">=3",
)
