# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json

from spack.cmd.read_external_db import entries_to_specs, compiler_from_entry


example_x_json_str = """\
{
  "name": "packagex",
  "hash": "hash-of-x",
  "prefix": "/path/to/packagex-install/",
  "version": "1.0",
  "arch": {
    "platform": "linux",
    "platform_os": "centos8",
    "target": {
      "name": "haswell"
    }
  },
  "compiler": {
    "name": "gcc",
    "version": "10.2.0"
  },
  "dependencies": {
    "packagey": {
      "hash": "hash-of-y",
      "type": ["link"]
    }
  },
  "parameters": {
    "precision": ["double", "float"]
  }
}
"""


example_compiler_entry = """\
{
  "name": "gcc",
  "prefix": "/path/to/compiler/",
  "version": "7.5.0",
  "arch": {
    "os": "centos8",
    "target": "x86_64"
  },
  "executables": {
    "cc": "/path/to/compiler/cc",
    "cxx": "/path/to/compiler/cxx",
    "fc": "/path/to/compiler/fc"
  }
}
"""


class JsonSpecEntry(object):
    def __init__(self, name, hash, prefix, version, arch, compiler,
                 dependencies, parameters):
        self.name = name
        self.hash = hash
        self.prefix = prefix
        self.version = version
        self.arch = arch
        self.compiler = compiler
        self.dependencies = dependencies
        self.parameters = parameters

    def to_dict(self):
        return {
            'name': self.name,
            'hash': self.hash,
            'prefix': self.prefix,
            'version': self.version,
            'arch': self.arch,
            'compiler': self.compiler,
            'dependencies': self.dependencies,
            'parameters': self.parameters
        }

    def as_dependency(self, deptypes):
        return (self.name,
                {'hash': self.hash,
                 'type': list(deptypes)})


class JsonArchEntry(object):
    def __init__(self, platform, os, target):
        self.platform = platform
        self.os = os
        self.target = target

    def to_dict(self):
        return {
            'platform': self.platform,
            'platform_os': self.os,
            'target': {
                'name': self.target
            }
        }


class JsonCompilerEntry(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def to_dict(self):
        return {
            'name': self.name,
            'version': self.version
        }


_common_arch = JsonArchEntry(
    platform='linux',
    os='centos8',
    target='haswell'
).to_dict()


_common_compiler = JsonCompilerEntry(
    name='gcc',
    version='10.2.0'
).to_dict()


def test_compatibility():
    """Make sure that JsonSpecEntry outputs the expected JSON structure
       by comparing it with JSON parsed from an example string. This
       ensures that the testing objects like JsonSpecEntry produce the
       same JSON structure as the expected file format.
    """
    y = JsonSpecEntry(
        name='packagey',
        hash='hash-of-y',
        prefix='/path/to/packagey-install/',
        version='1.0',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies={},
        parameters={}
    )

    x = JsonSpecEntry(
        name='packagex',
        hash='hash-of-x',
        prefix='/path/to/packagex-install/',
        version='1.0',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies=dict([y.as_dependency(deptypes=['link'])]),
        parameters={'precision': ['double', 'float']}
    )

    x_from_entry = x.to_dict()
    x_from_str = json.loads(example_x_json_str)
    assert x_from_entry == x_from_str


def test_compiler_from_entry():
    compiler_data = json.loads(example_compiler_entry)
    compiler_from_entry(compiler_data)


def generate_openmpi_entries():
    """Generate two example JSON entries that refer to an OpenMPI
       installation and a hwloc dependency.
    """
    hwloc = JsonSpecEntry(
        name='hwloc',
        hash='hwloc-fake-hash',
        prefix='/path/to/hwloc-install/',
        version='2.0.3',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies={},
        parameters={}
    )

    # This includes a variant which is guaranteed not to appear in the
    # OpenMPI package: we need to make sure we can use such package
    # descriptions.
    openmpi = JsonSpecEntry(
        name='openmpi',
        hash='openmpi-fake-hash',
        prefix='/path/to/packagex-install/',
        version='4.1.0',
        arch=_common_arch,
        compiler=_common_compiler,
        dependencies=dict([hwloc.as_dependency(deptypes=['link'])]),
        parameters={
            'internal-hwloc': False,
            'fabrics': ['psm'],
            'missing_variant': True
        }
    )

    return [openmpi, hwloc]


def test_spec_conversion():
    """Given JSON entries, check that we can form a set of Specs
       including dependency references.
    """
    entries = list(x.to_dict() for x in generate_openmpi_entries())
    specs = entries_to_specs(entries)
    openmpi_spec, = list(x for x in specs.values() if x.name == 'openmpi')
    assert openmpi_spec['hwloc']
