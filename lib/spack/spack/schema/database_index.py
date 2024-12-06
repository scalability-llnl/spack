# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for database index.json file

.. literalinclude:: _spack_root/lib/spack/spack/schema/database_index.py
   :lines: 17-
"""
from typing import Any, Dict

import spack.schema.spec

# spack.schema.spec.properties

properties: Dict[str, Any] = {
    "database": {
        "type": "object",
        "required": ["installs", "version"],
        "additionalProperties": False,
        "properties": {
            "installs": {
                "type": "object",
                "patternProperties": {
                    r"^[\w\d]{32}$": {
                        "type": "object",
                        "properties": {
                            "spec": spack.schema.spec.properties,
                            "path": {"oneOf": [{"type": "string"}, {"type": "null"}]},
                            "installed": {"type": "boolean"},
                            "ref_count": {"type": "integer", "minimum": 0},
                            "explicit": {"type": "boolean"},
                            "installation_time": {"type": "number"},
                        },
                    }
                },
            },
            "version": {"type": "string"},
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack spec schema",
    "type": "object",
    "required": ["database"],
    "additionalProperties": False,
    "properties": properties,
}
