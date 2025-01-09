# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Any, Dict

properties: Dict[str, Any] = {
    "develop": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "patternProperties": {
            r"\w[\w-]*": {
                "type": "object",
                "additionalProperties": False,
                "required": ["spec"],
                "properties": {"spec": {"type": "string"}, "path": {"type": "string"}},
            }
        },
    }
}


def update(data):
    return False


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack repository configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
