#!/bin/sh

# Upgrade pip
pip install --upgrade pip

pip install poetry

# Install the package
poetry install --no-root