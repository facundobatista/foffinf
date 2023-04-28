# Copyright 2023 Facundo Batista
# Licensed under the GPL v3 License
# For further info, check https://github.com/facundobatista/foffinf

"""Test how `formatize` affects the different loggers."""

import logging

import pytest

from foffinf import formatize


@pytest.mark.parametrize("scatter", [True, False])
def test_other_named(logs, scatter):
    """Formatize one, leave a named one in the old schema."""
    formatize("mylib.somemod1", scatter=scatter)

    logger1 = logging.getLogger("mylib.somemod1")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger("mylib.somemod2")
    logger2.info("logger2 %05d", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info


@pytest.mark.parametrize("scatter", [True, False])
def test_root(logs, scatter):
    """Formatize one, leave the root in the old schema."""
    formatize("mylib", scatter=scatter)

    logger1 = logging.getLogger("mylib")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger()
    logger2.info("logger2 %05d", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info


@pytest.mark.parametrize("scatter", [True, False])
def test_parent(logs, scatter):
    """Formatize one, leave the parent in the old schema."""
    formatize("foo.bar", scatter=scatter)

    logger1 = logging.getLogger("foo.bar")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger("foo")
    logger2.info("logger2 %05d", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info


@pytest.mark.parametrize("scatter", [True, False])
def test_sibling(logs, scatter):
    """Formatize one, leave the sibling in the old schema."""
    formatize("foo.bar", scatter=scatter)

    logger1 = logging.getLogger("foo.bar")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger("foo.baz")
    logger2.info("logger2 %05d", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info


def test_children_scatter_default(logs):
    """Formatize one, leave the children in the old schema."""
    formatize("foo")

    logger1 = logging.getLogger("foo")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger("foo.bar")
    logger2.info("logger2 %05d", 123)

    logger3 = logging.getLogger("foo.bar")
    logger3.info("logger3 %05d", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info
    assert "logger3 00123" in logs.info


def test_children_scatter_yes_simple(logs):
    """Formatize one and affect also all the children."""
    formatize("foo", scatter=True)

    logger1 = logging.getLogger("foo")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger("foo.bar")
    logger2.info("logger2 {:05d}", 123)

    logger3 = logging.getLogger("foo.bar")
    logger3.info("logger3 {:05d}", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info
    assert "logger3 00123" in logs.info


def test_children_scatter_yes_deep(logs):
    """Formatize one and affect also the child, deep structure."""
    formatize("aaa.bbb", scatter=True)

    logger1 = logging.getLogger("aaa.bbb")
    logger1.info("logger1 {:05d}", 123)

    logger2 = logging.getLogger("aaa.bbb.ccc")
    logger2.info("logger2 {:05d}", 123)

    logger3 = logging.getLogger("aaa.bbb.ccc.ddd.eee")
    logger3.info("logger3 {:05d}", 123)

    assert "logger1 00123" in logs.info
    assert "logger2 00123" in logs.info
    assert "logger3 00123" in logs.info
