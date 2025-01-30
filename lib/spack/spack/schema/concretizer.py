# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for concretizer.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/concretizer.py
   :lines: 12-
"""
from typing import Any, Dict

LIST_OF_SPECS = {"type": "array", "items": {"type": "string"}}

properties: Dict[str, Any] = {
    "concretizer": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "reuse": {
                "oneOf": [
                    {"type": "boolean"},
                    {"type": "string", "enum": ["dependencies"]},
                    {
                        "type": "object",
                        "properties": {
                            "roots": {"type": "boolean"},
                            "include": LIST_OF_SPECS,
                            "exclude": LIST_OF_SPECS,
                            "from": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "local",
                                                "buildcache",
                                                "external",
                                                "environment",
                                            ],
                                        },
                                        "path": {"type": "string"},
                                        "include": LIST_OF_SPECS,
                                        "exclude": LIST_OF_SPECS,
                                    },
                                },
                            },
                        },
                    },
                ]
            },
            "enable_node_namespace": {"type": "boolean"},
            "targets": {
                "type": "object",
                "properties": {
                    "host_compatible": {"type": "boolean"},
                    "granularity": {"type": "string", "enum": ["generic", "microarchitectures"]},
                },
            },
            "unify": {
                "oneOf": [{"type": "boolean"}, {"type": "string", "enum": ["when_possible"]}]
            },
            "splice": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "explicit": {
                        "type": "array",
                        "default": [],
                        "items": {
                            "type": "object",
                            "required": ["target", "replacement"],
                            "additionalProperties": False,
                            "properties": {
                                "target": {"type": "string"},
                                "replacement": {"type": "string"},
                                "transitive": {"type": "boolean", "default": False},
                            },
                        },
                    },
                    "automatic": {"type": "boolean"},
                },
            },
            "duplicates": {
                "type": "object",
                "properties": {
                    "strategy": {"type": "string", "enum": ["none", "minimal", "full"]}
                },
            },
            "timeout": {"type": "integer", "minimum": 0},
            "error_on_timeout": {"type": "boolean"},
            "os_compatible": {"type": "object", "additionalProperties": {"type": "array"}},
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack concretizer configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
