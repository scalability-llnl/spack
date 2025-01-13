# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for a buildcache spec.yaml file

.. literalinclude:: _spack_root/lib/spack/spack/schema/buildcache_spec.py
   :lines: 15-
"""
from typing import Any, Dict

import spack.schema.spec

properties: Dict[str, Any] = {
    # `buildinfo` is no longer needed as of Spack 0.21
    "buildinfo": {"type": "object"},
    "spec": {
        "type": "object",
        "additionalProperties": True,
        "items": spack.schema.spec.properties,
    },
    "binary_cache_checksum": {
        "type": "object",
        "properties": {"hash_algorithm": {"type": "string"}, "hash": {"type": "string"}},
    },
    "buildcache_layout_version": {"type": "number"},
    "archive_size": {"type": "number"},
    "archive_timestamp": {"type": "string"},
    "archive_compression": {"type": "string"},
}

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack buildcache specfile schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
