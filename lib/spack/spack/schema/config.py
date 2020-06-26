# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for config.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/config.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'config': {
        'type': 'object',
        'default': {},
        'properties': {
            'shared_linking': {
                'type': 'string',
                'enum': ['rpath', 'runpath']
            },
            'install_tree': {'type': 'string'},
            'install_hash_length': {'type': 'integer', 'minimum': 1},
            'install_path_scheme': {'type': 'string'},
            'build_stage': {
                'oneOf': [
                    {'type': 'string'},
                    {'type': 'array',
                     'items': {'type': 'string'}}],
            },
            'extensions': {
                'type': 'array',
                'items': {'type': 'string'}
            },
            'template_dirs': {
                'type': 'array',
                'items': {'type': 'string'}
            },
            'module_roots': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'tcl': {'type': 'string'},
                    'lmod': {'type': 'string'},
                    'dotkit': {'type': 'string'},
                },
                'deprecatedProperties': {
                    'properties': ['dotkit'],
                    'message': 'specifying a "{property}" module root has no '
                               'effect [support for {property} module files'
                               ' has been dropped]',
                    'error': False
                },
            },
            'source_cache': {'type': 'string'},
            'misc_cache': {'type': 'string'},
            'connect_timeout': {'type': 'integer', 'minimum': 0},
            'verify_ssl': {'type': 'boolean'},
            'suppress_gpg_warnings': {'type': 'boolean'},
            'install_missing_compilers': {'type': 'boolean'},
            'debug': {'type': 'boolean'},
            'checksum': {'type': 'boolean'},
            'locks': {'type': 'boolean'},
            'dirty': {'type': 'boolean'},
            'build_language': {'type': 'string'},
            'build_jobs': {'type': 'integer', 'minimum': 1},
            'ccache': {'type': 'boolean'},
            'db_lock_timeout': {'type': 'integer', 'minimum': 1},
            'package_lock_timeout': {
                'anyOf': [
                    {'type': 'integer', 'minimum': 1},
                    {'type': 'null'}
                ],
            },
            'metrics': {'type': 'boolean'},
            'metrcis_address': {
                'type': 'array',
                'items': {
                    'anyOf': [
                       {'type': 'string'},
                       {'type': 'integer'}
                    ]
                }
            },
            'allow_sgid': {'type': 'boolean'},
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack core configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
