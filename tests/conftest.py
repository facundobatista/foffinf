# Copyright 2023 Facundo Batista
# Licensed under the GPL v3 License
# For further info, check https://github.com/facundobatista/foffinf

import pytest

import foffinf


@pytest.fixture(autouse=True)
def clean_formatization():
    """Clean formatized structure between tests."""
    foffinf._formatized.clear()
