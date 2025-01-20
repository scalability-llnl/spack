# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for include.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/include.py
   :lines: 12-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "include": {
        "type": "array",
        "default": [],
        "additionalProperties": False,
        "items": {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "when": {"type": "string"},
                        "path": {"type": "string"},
                        "optional": {"type": "boolean"},
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
                {"type": "string"},
            ]
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack include configuration file schema",
    "properties": properties,
}
