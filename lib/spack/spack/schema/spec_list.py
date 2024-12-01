# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
matrix_schema = {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}

spec_list_schema = {
    "type": "array",
    "default": [],
    "items": {
        "anyOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "matrix": matrix_schema,
                    "exclude": {"type": "array", "items": {"type": "string"}},
                },
            },
            {"type": "string"},
            {"type": "null"},
        ]
    },
}
