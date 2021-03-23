# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple wrapper around JSON to guarantee consistent use of load/dump. """
import sys
import json
from six import string_types
from six import iteritems

import spack.error

__all__ = ['load', 'dump', 'SpackJSONError']

_json_dump_args = {
    'indent': True,
    'separators': (',', ': ')
}


def load(stream):
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, string_types):
        load = json.loads
    else:
        load = json.load

    return _strify(load(stream, object_hook=_strify), ignore_dicts=True)


def dump(data, stream=None):
    """Dump JSON with a reasonable amount of indentation and separation."""
    if stream is None:
        return json.dumps(data, **_json_dump_args)
    else:
        return json.dump(data, stream, **_json_dump_args)


def _strify(data, ignore_dicts=False):
    """Converts python 2 unicodes to str in JSON data."""
    # this is a no-op in python 3
    if sys.version_info[0] >= 3:
        return data

    # if this is a unicode string in python 2, return its string representation
    if isinstance(data, string_types):
        return data.encode('utf-8')

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_strify(item, ignore_dicts=True) for item in data]

    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return dict((_strify(key, ignore_dicts=True),
                     _strify(value, ignore_dicts=True)) for key, value in
                    iteritems(data))

    # if it's anything else, return it in its original form
    return data


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""

    def __init__(self, msg, json_error):
        super(SpackJSONError, self).__init__(msg, str(json_error))
