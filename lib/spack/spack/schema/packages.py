# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'packages': {
        'type': 'object',
        'default': {},
        'additionalProperties': False,
        'patternProperties': {
            r'\w[\w-]*': {  # package name
                'type': 'object',
                'default': {},
                'additionalProperties': False,
                'properties': {
                    'version': {
                        'type': 'array',
                        'default': [],
                        # version strings
                        'items': {'anyOf': [{'type': 'string'},
                                            {'type': 'number'}]}},
                    'target': {
                        'type': 'array',
                        'default': [],
                        # target names
                        'items': {'type': 'string'},
                    },
                    'compiler': {
                        'type': 'array',
                        'default': [],
                        'items': {'type': 'string'}},  # compiler specs
                    'buildable': {
                        'type':  'boolean',
                        'default': True,
                    },
                    'permissions': {
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': {
                            'read': {
                                'type':  'string',
                                'enum': ['user', 'group', 'world'],
                            },
                            'write': {
                                'type':  'string',
                                'enum': ['user', 'group', 'world'],
                            },
                            'group': {
                                'type':  'string',
                            },
                        },
                    },
                    'modules': {
                        'type': 'object',
                        'default': {},
                    },
                    'providers': {
                        'type':  'object',
                        'default': {},
                        'additionalProperties': False,
                        'patternProperties': {
                            r'\w[\w-]*': {
                                'type': 'array',
                                'default': [],
                                'items': {'type': 'string'}, }, }, },
                    'paths': {
                        'type': 'object',
                        'default': {},
                    },
                    'variants': {
                        'oneOf': [
                            {'type': 'string'},
                            {'type': 'array',
                             'items': {'type': 'string'}}],
                    },
                    'hardware': {
                        'type': 'array',
                        'additionalProperties': False,
                        'items': [{
                            'type': 'object',
                            'additionalProperties': False,
                            'properties': {
                                'host': {
                                    'type': 'object',
                                    'additionalProperties': False,
                                    'require': ['name', 'compiler'],
                                    'properties': {
                                        'name': {'type': 'string'},
                                        'compiler': {
                                            'type': 'array',
                                            'default': [],
                                            'items': {'type': 'string'}
                                        },
                                    }
                                }
                            }
                        }],
                    },
                },
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack package configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
