# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for view

.. literalinclude:: _spack_root/lib/spack/spack/schema/view.py
   :lines: 15-
"""
from typing import Any, Dict

import spack.schema
import spack.schema.projections

projections_scheme = spack.schema.projections.properties["projections"]

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "view": {
        "anyOf": [
            {"type": "boolean"},
            {"type": "string"},
            {
                "type": "object",
                "patternProperties": {
                    r"\w+": {
                        "required": ["root"],
                        "additionalProperties": False,
                        "properties": {
                            "root": {"type": "string"},
                            "link": {"type": "string", "pattern": "(roots|all|run)"},
                            "link_type": {"type": "string"},
                            "select": {"type": "array", "items": {"type": "string"}},
                            "exclude": {"type": "array", "items": {"type": "string"}},
                            "projections": projections_scheme,
                        },
                    }
                },
            },
        ]
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack view configuration file schema",
    "properties": properties,
}
