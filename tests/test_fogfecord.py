# Copyright 2023 Facundo Batista
# Licensed under the GPL v3 License
# For further info, check https://github.com/facundobatista/foffinf

"""Test the _FogFecord behaviour."""

import logging

from foffinf import formatize


def test_args_none(logs):
    """Log without arguments."""
    formatize("mylib")
    logger = logging.getLogger("mylib")

    logger.info("testlogger")
    assert "testlogger" in logs.info


def test_args_one(logs):
    """Log using one argument."""
    formatize("mylib")
    logger = logging.getLogger("mylib")

    logger.info("testlogger {:05d}", 123)
    assert "testlogger 00123" in logs.info


def test_args_many(logs):
    """Log using multiple arguments."""
    formatize("mylib")
    logger = logging.getLogger("mylib")

    logger.info("testlogger {:05d} {} {!r}", 123, "foo", 37)
    assert "testlogger 00123 foo 37" in logs.info


def test_error(logs):
    """Produce logs even if there is an error."""
    formatize("mylib")
    logger = logging.getLogger("mylib")

    logger.info("test logger {:05d}", 123, "onetoomany")  # this will fail, but not crash!
    logger.info("continued after bad log call")
    assert "continued after bad log call" in logs.info
