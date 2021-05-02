# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for hardware.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/hardware.py
   :lines: 11-
"""
#: Properties for inclusion in other schemas
properties = {
    'hardware': {
        'type': 'object',
        'additionalProperties': False,
        'required': ['hosts'],
        'properties': {
            'hosts': {
                'type': 'array',
                'items': [{
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'host': {
                            'type': 'object',
                            'additionalProperties': False,
                            'required': ['name', 'target', 'operating_system'],
                            'properties': {
                                'name': {'type': 'string'},
                                'operating_system': {'type': 'string'},
                                'target': {'type': 'string'}
                            }
                        }
                    }
                }]
            }
        }

    }
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack hardware configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
