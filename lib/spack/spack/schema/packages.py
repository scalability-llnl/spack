# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 14-
"""
from typing import Any, Dict

import spack.schema.environment

from .compilers import extra_rpaths, flags, implicit_rpaths

permissions = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "read": {"type": "string", "enum": ["user", "group", "world"]},
        "write": {"type": "string", "enum": ["user", "group", "world"]},
        "group": {"type": "string"},
    },
}

variants = {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]}

requirements = {
    "oneOf": [
        # 'require' can be a list of requirement_groups.
        # each requirement group is a list of one or more
        # specs. Either at least one or exactly one spec
        # in the group must be satisfied (depending on
        # whether you use "any_of" or "one_of",
        # repectively)
        {
            "type": "array",
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "one_of": {"type": "array", "items": {"type": "string"}},
                            "any_of": {"type": "array", "items": {"type": "string"}},
                            "spec": {"type": "string"},
                            "message": {"type": "string"},
                            "when": {"type": "string"},
                        },
                    },
                    {"type": "string"},
                ]
            },
        },
        # Shorthand for a single requirement group with
        # one member
        {"type": "string"},
    ]
}

prefer_and_conflict = {
    "type": "array",
    "items": {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "spec": {"type": "string"},
                    "message": {"type": "string"},
                    "when": {"type": "string"},
                },
            },
            {"type": "string"},
        ]
    },
}

permissions = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "read": {"type": "string", "enum": ["user", "group", "world"]},
        "write": {"type": "string", "enum": ["user", "group", "world"]},
        "group": {"type": "string"},
    },
}

package_attributes = {
    "type": "object",
    "additionalProperties": False,
    "patternProperties": {r"\w+": {}},
}

REQUIREMENT_URL = "https://spack.readthedocs.io/en/latest/packages_yaml.html#package-requirements"

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "packages": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": {
            "all": {  # package name
                "type": "object",
                "default": {},
                "additionalProperties": False,
                "properties": {
                    "require": requirements,
                    "prefer": prefer_and_conflict,
                    "conflict": prefer_and_conflict,
                    "target": {
                        "type": "array",
                        "default": [],
                        # target names
                        "items": {"type": "string"},
                    },
                    "compiler": {
                        "type": "array",
                        "default": [],
                        "items": {"type": "string"},
                    },  # compiler specs
                    "buildable": {"type": "boolean", "default": True},
                    "permissions": permissions,
                    # If 'get_full_repo' is promoted to a Package-level
                    # attribute, it could be useful to set it here
                    "package_attributes": package_attributes,
                    "providers": {
                        "type": "object",
                        "default": {},
                        "additionalProperties": False,
                        "patternProperties": {
                            r"\w[\w-]*": {
                                "type": "array",
                                "default": [],
                                "items": {"type": "string"},
                            }
                        },
                    },
                    "variants": variants,
                },
            }
        },
        "patternProperties": {
            r"(?!^all$)(^\w[\w-]*)": {  # package name
                "type": "object",
                "default": {},
                "additionalProperties": False,
                "properties": {
                    "require": requirements,
                    "prefer": prefer_and_conflict,
                    "conflict": prefer_and_conflict,
                    "version": {
                        "type": "array",
                        "default": [],
                        # version strings
                        "items": {"anyOf": [{"type": "string"}, {"type": "number"}]},
                    },
                    "buildable": {"type": "boolean", "default": True},
                    "permissions": permissions,
                    # If 'get_full_repo' is promoted to a Package-level
                    # attribute, it could be useful to set it here
                    "package_attributes": package_attributes,
                    "variants": variants,
                    "externals": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "spec": {"type": "string"},
                                "prefix": {"type": "string"},
                                "modules": {"type": "array", "items": {"type": "string"}},
                                "extra_attributes": {
                                    "type": "object",
                                    "additionalProperties": True,
                                    "properties": {
                                        "compilers": {
                                            "type": "object",
                                            "patternProperties": {
                                                r"(^\w[\w-]*)": {"type": "string"}
                                            },
                                        },
                                        "environment": spack.schema.environment.definition,
                                        "extra_rpaths": extra_rpaths,
                                        "implicit_rpaths": implicit_rpaths,
                                        "flags": flags,
                                    },
                                },
                            },
                            "additionalProperties": True,
                            "required": ["spec"],
                        },
                    },
                },
            }
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack package configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data):
    changed = False
    for key in data:
        version = data[key].get("version")
        if not version or all(isinstance(v, str) for v in version):
            continue

        data[key]["version"] = [str(v) for v in version]
        changed = True

    return changed
