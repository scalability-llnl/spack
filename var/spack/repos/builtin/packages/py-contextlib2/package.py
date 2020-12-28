# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyContextlib2(PythonPackage):
    """contextlib2 is a backport of the standard library's contextlib module to
    earlier Python versions."""

    homepage = "https://contextlib2.readthedocs.io/en/stable/"
    url      = "https://github.com/jazzband/contextlib2/archive/v0.6.0.tar.gz"

    version('0.6.0', sha256='4f18e2f28bb642aae9447aacec93b1319c8ee838711553c0a2bd906753f2ad33')
    version('0.5.5', sha256='613569263db0271f34c8484792360272a731f2185567c31c8118e9c994412170')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
