# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 13-
"""


# env modification - e.g.: ["append_path", "PATH", "/some/path"]
env_modification = {'type': 'array', 'items': {'type': 'string'}}


# env modification entry - either an env modification, or a dict.
#     If a dict, its keys can only be "build" or "run", and the value is a
#     list of env modifications.
#
# e.g.:
#
# build:
#   - ["append_path", "CMAKE_MODULE_PATH", "/some/path"]
#   - ["unset", "VAR0", "VAR1"]
#
# This type allows for a list of env modification entries to look like this:
#
# env:
#   - ["append_path", "PATH", "/some/path"]
#   - ["append_path", "PATH", "/some/path"]
#   - [... etc ... ]
#
#   - build:
#       - ["append_path", "CMAKE_MODULE_PATH", "/some/path"]
#       - ["unset", "VAR0", "VAR1"]
#       - [ ... other build-only settings ]
#       - [ ... other build-only settings ]
#
#   - run:
#       - ["append_path", "CMAKE_MODULE_PATH", "/some/path"]
#       - ["unset", "VAR0", "VAR1"]
#       - [ ... other run-only settings ]
#       - [ ... other run-only settings ]
#
#   - [ ... other common env settings ... ]
#   - [ ... other common env settings ... ]
env_mod_entry = {
    'anyOf': [
        env_modification,
        {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'build': {
                    'type': 'array',
                    'default': [],
                    'items': env_modification,
                },
                'run': {
                    'type': 'array',
                    'default': [],
                    'items': env_modification,
                },
            }
        },
    ]
}


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
                    'env': {
                        'type': 'object',
                        'default': {},
                        'additionalProperties': False,
                        'patternProperties': {
                            r'\w[\w-]*': {
                                'type': 'array',
                                'default': [],
                                'items': env_mod_entry,
                            },
                        },
                    },
                    'variants': {
                        'oneOf': [
                            {'type': 'string'},
                            {'type': 'array',
                             'items': {'type': 'string'}}],
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
