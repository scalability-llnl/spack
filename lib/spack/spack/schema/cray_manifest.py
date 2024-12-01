# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for Cray descriptive manifest: this describes a set of
   installed packages on the system and also specifies dependency
   relationships between them (so this provides more information than
   external entries in packages configuration).

   This does not specify a configuration - it is an input format
   that is consumed and transformed into Spack DB records.
"""
from typing import Any, Dict

properties: Dict[str, Any] = {
    "_meta": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "file-type": {"type": "string", "minLength": 1},
            "cpe-version": {"type": "string", "minLength": 1},
            "system-type": {"type": "string", "minLength": 1},
            "schema-version": {"type": "string", "minLength": 1},
            # Older schemas use did not have "cpe-version", just the
            # schema version; in that case it was just called "version"
            "version": {"type": "string", "minLength": 1},
        },
    },
    "compilers": {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "version": {"type": "string", "minLength": 1},
                "prefix": {"type": "string", "minLength": 1},
                "executables": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "cc": {"type": "string", "minLength": 1},
                        "cxx": {"type": "string", "minLength": 1},
                        "fc": {"type": "string", "minLength": 1},
                    },
                },
                "arch": {
                    "type": "object",
                    "required": ["os", "target"],
                    "additionalProperties": False,
                    "properties": {
                        "os": {"type": "string", "minLength": 1},
                        "target": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    },
    "specs": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["name", "version", "arch", "compiler", "prefix", "hash"],
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "version": {"type": "string", "minLength": 1},
                "arch": {
                    "type": "object",
                    "required": ["platform", "platform_os", "target"],
                    "additionalProperties": False,
                    "properties": {
                        "platform": {"type": "string", "minLength": 1},
                        "platform_os": {"type": "string", "minLength": 1},
                        "target": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["name"],
                            "properties": {"name": {"type": "string", "minLength": 1}},
                        },
                    },
                },
                "compiler": {
                    "type": "object",
                    "required": ["name", "version"],
                    "additionalProperties": False,
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "version": {"type": "string", "minLength": 1},
                    },
                },
                "dependencies": {
                    "type": "object",
                    "patternProperties": {
                        "\\w[\\w-]*": {
                            "type": "object",
                            "required": ["hash"],
                            "additionalProperties": False,
                            "properties": {
                                "hash": {"type": "string", "minLength": 1},
                                "type": {
                                    "type": "array",
                                    "items": {"type": "string", "minLength": 1},
                                },
                            },
                        }
                    },
                },
                "prefix": {"type": "string", "minLength": 1},
                "rpm": {"type": "string", "minLength": 1},
                "hash": {"type": "string", "minLength": 1},
                "parameters": {"type": "object"},
            },
        },
    },
}

schema = {
    "$schema": "http://json-schema.org/schema#",
    "title": "CPE manifest schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
