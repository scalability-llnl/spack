# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnittest2(PythonPackage):
    """unittest2 is a backport of the new features added to the unittest
    testing framework in Python 2.7 and onwards."""

    homepage = "https://pypi.python.org/pypi/unittest2"
    url      = "https://pypi.io/packages/source/u/unittest2/unittest2-1.1.0.tar.gz"

    version('1.1.0', sha256='22882a0e418c284e1f718a822b3b022944d53d2d908e1690b319a9d3eb2c0579')

    depends_on('py-setuptools', type='build')
    depends_on('py-traceback2', type=('build', 'run'))
    depends_on('py-six@1.4:', type=('build', 'run'))
    depends_on('py-argparse', type=('build', 'run'))
