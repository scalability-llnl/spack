# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "upstreams": {
        "type": "object",
        "default": {},
        "patternProperties": {
            r"\w[\w-]*": {
                "type": "object",
                "default": {},
                "additionalProperties": False,
                "properties": {
                    "install_tree": {"type": "string"},
                    "modules": {
                        "type": "object",
                        "properties": {"tcl": {"type": "string"}, "lmod": {"type": "string"}},
                    },
                },
            }
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack core configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
