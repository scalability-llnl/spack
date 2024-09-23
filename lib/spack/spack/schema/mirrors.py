# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/mirrors.py
   :lines: 13-
"""
from typing import Any, Dict

string_or_variable = {
    "oneOf": [
        {
            "type": "object",
            "required": ["variable"],
            "additionalProperties": False,
            "properties": {"variable": {"type": "string"}},
        },
        {"type": "string"},
    ]
}


#: Common properties for connection specification
connection = {
    "url": {"type": "string"},
    # todo: replace this with named keys "username" / "password" or "id" / "secret"
    "access_pair": {
        "oneOf": [
            {
                "type": "array",
                "items": {"minItems": 2, "maxItems": 2, **string_or_variable},
            },  # deprecated
            {
                "type": "object",
                "required": ["secret_variable"],
                # Only allow id or id_variable to be set, not both
                "oneOf": [{"required": ["id"]}, {"required": ["id_variable"]}],
                "properties": {
                    "id": {"type": "string"},
                    "id_variable": {"type": "string"},
                    "secret_variable": {"type": "string"},
                },
            },
        ]
    },
    "profile": {"type": ["string", "null"]},
    "endpoint_url": {"type": ["string", "null"]},
    "access_token": {"type": ["string", "null"]},  # deprecated
    "access_token_variable": {"type": ["string", "null"]},
}

connection_ext = {
    "deprecatedProperties": [
        {
            "names": ["access_token"],
            "message": "Spack no longer supportes plain text access_token in mirror configs",
            "error": False,
        }
    ]
}


#: Mirror connection inside pull/push keys
fetch_and_push = {
    "anyOf": [
        {"type": "string"},
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {**connection},  # type: ignore
            **connection_ext,  # type: ignore
        },
    ]
}

#: Mirror connection when no pull/push keys are set
mirror_entry = {
    "type": "object",
    "additionalProperties": False,
    "anyOf": [{"required": ["url"]}, {"required": ["fetch"]}, {"required": ["pull"]}],
    "properties": {
        "source": {"type": "boolean"},
        "binary": {"type": "boolean"},
        "signed": {"type": "boolean"},
        "fetch": fetch_and_push,
        "push": fetch_and_push,
        "autopush": {"type": "boolean"},
        **connection,  # type: ignore
    },
    **connection_ext,  # type: ignore
}

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "mirrors": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "patternProperties": {r"\w[\w-]*": {"anyOf": [{"type": "string"}, mirror_entry]}},
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack mirror configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data):
    import warnings

    import jsonschema

    errors = []

    def check_access_pair(name, section):
        if not section or not isinstance(section, dict):
            return

        access_pair = section.get("access_pair")
        if access_pair and isinstance(access_pair, list):
            warnings.warn(
                f"{name}: Using access_pair with a list is "
                "deprecated, prefer id/secret_variable keys"
            )
            if not isinstance(access_pair[1], dict):
                warnings.warn(f"{name}: Secret part of access pair should be a variable")

        if set(["access_token", "access_token_variable"]).issubset(set(section.keys())):
            errors.append(
                f'{name}: mirror credential "access_token" conflicts with "access_token_variable"'
            )

    # Check all of the sections
    for name, section in data.items():
        check_access_pair(name, section)
        if isinstance(section, dict):
            check_access_pair(name, section.get("fetch"))
            check_access_pair(name, section.get("push"))

    if errors:
        raise jsonschema.ValidationError("\n".join(errors))
