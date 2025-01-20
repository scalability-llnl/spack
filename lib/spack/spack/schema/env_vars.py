# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for env_vars.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env_vars.py
   :lines: 15-
"""
from typing import Any, Dict

import spack.schema.environment

properties: Dict[str, Any] = {"env_vars": spack.schema.environment.definition}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack env_vars configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
