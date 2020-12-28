# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmmap(PythonPackage):
    """
    A pure Python implementation of a sliding window memory map manager
    """

    homepage = "https://github.com/gitpython-developers/smmap"
    url      = "https://pypi.io/packages/source/s/smmap/smmap-3.0.4.tar.gz"

    version('3.0.4', sha256='9c98bbd1f9786d22f14b3d4126894d56befb835ec90cef151af566c7e19b5d24')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
