# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for projections.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/projections.py
   :lines: 14-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "projections": {"type": "object", "patternProperties": {r"all|\w[\w-]*": {"type": "string"}}}
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack view projection configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
