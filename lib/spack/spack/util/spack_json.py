# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple wrapper around JSON to guarantee consistent use of load/dump. """
import json
from typing import Any, Dict, Optional

import spack.error

__all__ = ["load", "dump", "SpackJSONError"]

_json_dump_args = {"indent": None, "separators": (",", ":")}


def load(stream: Any) -> Dict:
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, str):
        return json.loads(stream)
    return json.load(stream)


def dump(data: Dict, stream: Optional[Any] = None) -> Optional[str]:
    """Dump JSON with a reasonable amount of indentation and separation."""
    if stream is None:
        return json.dumps(data, **_json_dump_args)  # type: ignore[arg-type]
    json.dump(data, stream, **_json_dump_args)  # type: ignore[arg-type]
    return None


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""

    def __init__(self, msg: str, json_error: BaseException):
        super().__init__(msg, str(json_error))
