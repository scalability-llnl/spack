# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for compilers.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/compilers.py
   :lines: 15-
"""
from typing import Any, Dict

import spack.schema.environment

flags: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "cflags": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "cxxflags": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "fflags": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "cppflags": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "ldflags": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "ldlibs": {"anyOf": [{"type": "string"}, {"type": "null"}]},
    },
}


extra_rpaths: Dict[str, Any] = {"type": "array", "default": [], "items": {"type": "string"}}

implicit_rpaths: Dict[str, Any] = {
    "anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "boolean"}]
}

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "compilers": {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "compiler": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["paths", "spec", "modules", "operating_system"],
                    "properties": {
                        "paths": {
                            "type": "object",
                            "required": ["cc", "cxx", "f77", "fc"],
                            "additionalProperties": False,
                            "properties": {
                                "cc": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "cxx": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "f77": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "fc": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                            },
                        },
                        "flags": flags,
                        "spec": {"type": "string"},
                        "operating_system": {"type": "string"},
                        "target": {"type": "string"},
                        "alias": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "modules": {
                            "anyOf": [{"type": "string"}, {"type": "null"}, {"type": "array"}]
                        },
                        "implicit_rpaths": implicit_rpaths,
                        "environment": spack.schema.environment.definition,
                        "extra_rpaths": extra_rpaths,
                    },
                }
            },
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack compiler configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
