# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyRuamelYamlClib(PythonPackage):
    """C version of reader, parser and emitter for ruamel.yaml derived from
    libyaml."""

    homepage = "https://bitbucket.org/ruamel/yaml.clib"
    url      = "https://pypi.io/packages/source/r/ruamel.yaml.clib/ruamel.yaml.clib-0.2.0.tar.gz"

    version('0.2.0', sha256='b66832ea8077d9b3f6e311c4a53d06273db5dc2db6e8a908550f3c14d67e718c')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools@28.7.0:', type='build')
