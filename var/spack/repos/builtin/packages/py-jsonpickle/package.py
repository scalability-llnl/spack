# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyJsonpickle(PythonPackage):
    """Python library for serializing any arbitrary object graph into JSON."""

    homepage = "https://github.com/jsonpickle/jsonpickle"
    url      = "https://pypi.io/packages/source/j/jsonpickle/jsonpickle-1.4.1.tar.gz"

    version('1.4.1', sha256='e8d4b7cd0bd6826001a74377df1079a76ad8bae0f909282de2554164c837c8ba')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@3.4.1:+toml', type='build')
    depends_on('py-importlib-metadata', type=('build', 'run'))
