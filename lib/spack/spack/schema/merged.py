# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for configuration merged into one file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/merged.py
   :lines: 39-
"""
from llnl.util.lang import union_dicts

import spack.schema.cdash
import spack.schema.compilers
import spack.schema.config
import spack.schema.container
import spack.schema.gitlab_ci
import spack.schema.hardware
import spack.schema.mirrors
import spack.schema.modules
import spack.schema.packages
import spack.schema.repos
import spack.schema.upstreams


#: Properties for inclusion in other schemas
properties = union_dicts(
    spack.schema.cdash.properties,
    spack.schema.compilers.properties,
    spack.schema.config.properties,
    spack.schema.container.properties,
    spack.schema.gitlab_ci.properties,
    spack.schema.hardware.properties,
    spack.schema.mirrors.properties,
    spack.schema.modules.properties,
    spack.schema.packages.properties,
    spack.schema.repos.properties,
    spack.schema.upstreams.properties
)


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack merged configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
