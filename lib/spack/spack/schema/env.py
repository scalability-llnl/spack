# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 36-
"""
import warnings

from llnl.util.lang import union_dicts

import spack.schema.merged
import spack.schema.packages
import spack.schema.projections

#: legal first keys in the schema
keys = ('spack', 'env')

spec_list_schema = {
    'type': 'array',
    'default': [],
    'items': {
        'anyOf': [
            {'type': 'object',
             'additionalProperties': False,
             'properties': {
                 'matrix': {
                     'type': 'array',
                     'items': {
                         'type': 'array',
                         'items': {
                             'type': 'string',
                         }
                     }
                 },
                 'exclude': {
                     'type': 'array',
                     'items': {
                         'type': 'string'
                     }
                 }
             }},
            {'type': 'string'},
            {'type': 'null'}
        ]
    }
}

projections_scheme = spack.schema.projections.properties['projections']

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack environment file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        '^env|spack$': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': union_dicts(
                # merged configuration scope schemas
                spack.schema.merged.properties,
                # extra environment schema properties
                {
                    'include': {
                        'type': 'array',
                        'default': [],
                        'items': {
                            'type': 'string'
                        },
                    },
                    'develop': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'spec': {'type': 'string'},
                                'path': {'type': 'string'}
                            },
                            'additionalProperties': False,
                            'required': ['spec']
                        }
                    },
                    'definitions': {
                        'type': 'array',
                        'default': [],
                        'items': {
                            'type': 'object',
                            'properties': {
                                'when': {
                                    'type': 'string'
                                }
                            },
                            'patternProperties': {
                                r'^(?!when$)\w*': spec_list_schema
                            }
                        }
                    },
                    'specs': spec_list_schema,
                    'view': {
                        'anyOf': [
                            {'type': 'boolean'},
                            {'type': 'string'},
                            {
                                'type': 'object',
                                'patternProperties': {
                                    r'\w+': {
                                        'required': ['root'],
                                        'additionalProperties': False,
                                        'properties': {
                                            'root': {
                                                'type': 'string'
                                            },
                                            'link': {
                                                'type': 'string',
                                                'pattern': '(roots|all)',
                                            },
                                            'select': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                }
                                            },
                                            'exclude': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                }
                                            },
                                            'projections': projections_scheme
                                        }
                                    }
                                }
                            }
                        ]
                    },
                    'concretization': {
                        'type': 'string',
                        'enum': ['together', 'separately'],
                        'default': 'separately'
                    }
                }
            )
        }
    }
}


def update(data):
    """Update the data in place to remove deprecated properties.

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """
    if 'include' in data:
        msg = ("included configuration files should be updated manually"
               " [files={0}]")
        warnings.warn(msg.format(', '.join(data['include'])))

    if 'packages' in data:
        return spack.schema.packages.update(data['packages'])
    return False
