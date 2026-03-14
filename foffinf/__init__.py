# Copyright 2023-2026 Facundo Batista
# Licensed under the GPL v3 License
# For further info, check https://github.com/facundobatista/foffinf

"""Main foffinf module."""

import collections
import logging


class _FogFecord(logging.LogRecord):
    """An f-oriented log record factory."""

    def getMessage(self):
        """Return the message for this LogRecord but building it with .format."""
        msg = str(self.msg)
        if self.args:
            if isinstance(self.args, collections.abc.Mapping):
                # the arguments is not the regular sequence of values, but changed by LogRecord
                # to just hold the dictionary, in case the user wants to pass a message with
                # named replacements (e.g. '{foo} {bar}'; try that replacement, and if it fails
                # fallback to using the dictionary as the single value
                try:
                    msg = msg.format(**self.args)
                except IndexError:
                    msg = msg.format(self.args)
            else:
                msg = msg.format(*self.args)
        return msg


_formatized = {}


def _factory(name, *a, **k):
    """Create one or the other log record according to the name."""
    klass = logging.LogRecord
    if name in _formatized:
        klass = _FogFecord
    else:
        tmp_name = name
        while "." in tmp_name:
            tmp_name, _ = tmp_name.rsplit(".", 1)
            if _formatized.get(tmp_name, False):
                # the parent is formatized and ok to scatter
                klass = _FogFecord
                break

    return klass(name, *a, **k)


logging.setLogRecordFactory(_factory)


def formatize(name: str, scatter: bool = False):
    """Mark the name to use 'format' to later decide which log record to use."""
    _formatized[name] = scatter
