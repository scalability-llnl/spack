# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for a buildcache spec.yaml file

.. literalinclude:: _spack_root/lib/spack/spack/schema/buildcache_spec.py
   :lines: 14-
"""
import spack.schema.spec


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack buildcache spec.yaml schema',
    'type': 'object',
    # 'additionalProperties': True,
    'properties': {
        'buildinfo': {
            'type': 'object',
            'additionalProperties': False,
            'required': ['relative_prefix'],
            'properties': {
                'relative_prefix': {'type': 'string'},
                'relative_rpaths': {'type': 'boolean'},
            },
        },
        'spec': {
            'type': 'array',
            'items': spack.schema.spec.properties,
        },
        'binary_cache_checksum': {
            'type': 'object',
            'properties': {
                'hash_algorithm': {'type': 'string'},
                'hash': {'type': 'string'},
            },
        },
    },
}
