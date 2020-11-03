# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for a spec found in spec.yaml or database index.json files

.. literalinclude:: _spack_root/lib/spack/spack/schema/spec.py
   :lines: 13-
"""


target = {
    'oneOf': [
        {
            'type': 'string',
        }, {
            'type': 'object',
            'additionalProperties': False,
            'required': [
                'name',
                'vendor',
                'features',
                'generation',
                'parents',
            ],
            'properties': {
                'name': {'type': 'string'},
                'vendor': {'type': 'string'},
                'features': {
                    'type': 'array',
                    'items': {'type': 'string'},
                },
                'generation': {'type': 'integer'},
                'parents': {
                    'type': 'array',
                    'items': {'type': 'string'},
                },
            },
        },
    ],
}

arch = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'platform': {},
        'platform_os': {},
        'target': target,
    },
}

dependencies = {
    'type': 'object',
    'patternProperties': {
        r'\w[\w-]*': {  # package name
            'type': 'object',
            'properties': {
                'hash': {'type': 'string'},
                'type': {
                    'type': 'array',
                    'items': {'type': 'string'},
                },
            },
        },
    },
}

#: Properties for inclusion in other schemas
properties = {
    r'\w[\w-]*': {  # package name
        'type': 'object',
        'additionalProperties': False,
        'required': [
            'version',
            'arch',
            'compiler',
            'namespace',
            'parameters',
        ],
        'properties': {
            'hash': {'type': 'string'},
            'full_hash': {'type': 'string'},
            'version': {
                'oneOf': [
                    {'type': 'string'},
                    {'type': 'number'},
                ],
            },
            'arch': arch,
            'compiler': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'name': {'type': 'string'},
                    'version': {'type': 'string'},
                },
            },
            'develop': {
                'anyOf': [
                    {'type': 'boolean'},
                    {'type': 'string'},
                ],
            },
            'namespace': {'type': 'string'},
            'parameters': {
                'type': 'object',
                'required': [
                    'cflags',
                    'cppflags',
                    'cxxflags',
                    'fflags',
                    'ldflags',
                    'ldlibs',
                ],
                'additionalProperties': True,
                'properties': {
                    'patches': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'cflags': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'cppflags': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'cxxflags': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'fflags': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'ldflags': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                    'ldlib': {
                        'type': 'array',
                        'items': {'type': 'string'},
                    },
                },
            },
            'patches': {
                'type': 'array',
                'items': {},
            },
            'dependencies': dependencies,
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack spec schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': properties,
}
