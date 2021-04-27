# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyJsonpathNg(PythonPackage):
    """A final implementation of JSONPath for Python that aims to be
    standard compliant, including arithmetic and binary comparison
    operators."""

    homepage = "https://github.com/h2non/jsonpath-ng"
    pypi     = "jsonpath-ng/jsonpath-ng-1.5.2.tar.gz"

    version('1.5.2', sha256='144d91379be14d9019f51973bd647719c877bfc07dc6f3f5068895765950c69d')

    depends_on('py-setuptools', type='build')
    depends_on('py-ply', type=('build', 'run'))
    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
