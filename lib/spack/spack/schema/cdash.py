# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for cdash.yaml configuration file.

.. literalinclude:: ../spack/schema/cdash.py
   :lines: 13-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "cdash": {
        "type": "object",
        "additionalProperties": False,
        "required": ["upload-url"],
        "patternProperties": {
            r"buildstamp": {"type": "string"},
            r"build": {"type": "string"},
            r"upload-url": {"type": "string"},
            r"site": {"type": "string"},
            r"track": {"type": "string"},
        },
        "anyOf": [
            {
                "required": ["upload-url"],
                "not": {"required": ["track", "buildstamp"]}
            },
            {
                "required": ["upload-url", "track"],
                "not": {"required": ["buildstamp"]}
            },
            {
                "required": ["upload-url", "buildstamp"],
                "not": {"required": ["track"]}
            }
        ]
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack cdash configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
