# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for configuration merged into one file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/merged.py
   :lines: 32-
"""
from typing import Any, Dict

from llnl.util.lang import union_dicts

import spack.schema.bootstrap
import spack.schema.cdash
import spack.schema.ci
import spack.schema.compilers
import spack.schema.concretizer
import spack.schema.config
import spack.schema.container
import spack.schema.definitions
import spack.schema.develop
import spack.schema.mirrors
import spack.schema.modules
import spack.schema.packages
import spack.schema.repos
import spack.schema.upstreams
import spack.schema.view

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = union_dicts(
    spack.schema.bootstrap.properties,
    spack.schema.cdash.properties,
    spack.schema.compilers.properties,
    spack.schema.concretizer.properties,
    spack.schema.config.properties,
    spack.schema.container.properties,
    spack.schema.ci.properties,
    spack.schema.definitions.properties,
    spack.schema.develop.properties,
    spack.schema.mirrors.properties,
    spack.schema.modules.properties,
    spack.schema.packages.properties,
    spack.schema.repos.properties,
    spack.schema.upstreams.properties,
    spack.schema.view.properties,
)


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack merged configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
