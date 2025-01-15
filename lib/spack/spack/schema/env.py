# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 19-
"""
from typing import Any, Dict

from llnl.util.lang import union_dicts

import spack.schema.merged

from .spec_list import spec_list_schema

#: Top level key in a manifest file
TOP_LEVEL_KEY = "spack"

include_concrete = {"type": "array", "default": [], "items": {"type": "string"}}

properties: Dict[str, Any] = {
    "spack": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": union_dicts(
            # merged configuration scope schemas
            spack.schema.merged.properties,
            # extra environment schema properties
            {
                "include": {"type": "array", "default": [], "items": {"type": "string"}},
                "specs": spec_list_schema,
                "include_concrete": include_concrete,
            },
        ),
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack environment file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data):
    """Update the data in place to remove deprecated properties.

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """
    # There are not currently any deprecated attributes in this section
    # that have not been removed
    return False
