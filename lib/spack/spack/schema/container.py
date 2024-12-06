# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for the 'container' subsection of Spack environments."""
from typing import Any, Dict

_stages_from_dockerhub = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "os": {"type": "string"},
        "spack": {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "additional_properties": False,
                    "properties": {
                        "url": {"type": "string"},
                        "ref": {"type": "string"},
                        "resolve_sha": {"type": "boolean", "default": False},
                        "verify": {"type": "boolean", "default": False},
                    },
                },
            ]
        },
    },
    "required": ["os", "spack"],
}

_custom_stages = {
    "type": "object",
    "additionalProperties": False,
    "properties": {"build": {"type": "string"}, "final": {"type": "string"}},
    "required": ["build", "final"],
}

#: List of packages for the schema below
_list_of_packages = {"type": "array", "items": {"type": "string"}}

#: Schema for the container attribute included in Spack environments
container_schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        # The recipe formats that are currently supported by the command
        "format": {"type": "string", "enum": ["docker", "singularity"]},
        # Describes the base image to start from and the version
        # of Spack to be used
        "images": {"anyOf": [_stages_from_dockerhub, _custom_stages]},
        # Whether or not to strip installed binaries
        "strip": {"type": "boolean", "default": True},
        # Additional system packages that are needed at runtime
        "os_packages": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": ["apt", "yum", "zypper", "apk", "yum_amazon"],
                },
                "update": {"type": "boolean"},
                "build": _list_of_packages,
                "final": _list_of_packages,
            },
            "additionalProperties": False,
        },
        # Add labels to the image
        "labels": {"type": "object"},
        # Use a custom template to render the recipe
        "template": {"type": "string", "default": None},
        # Reserved for properties that are specific to each format
        "singularity": {
            "type": "object",
            "additionalProperties": False,
            "default": {},
            "properties": {
                "runscript": {"type": "string"},
                "startscript": {"type": "string"},
                "test": {"type": "string"},
                "help": {"type": "string"},
            },
        },
        "docker": {"type": "object", "additionalProperties": False, "default": {}},
        "depfile": {"type": "boolean", "default": False},
    },
}

properties: Dict[str, Any] = {"container": container_schema}
