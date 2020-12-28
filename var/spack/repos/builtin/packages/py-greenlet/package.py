# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGreenlet(PythonPackage):
    """Lightweight in-process concurrent programming"""

    homepage = "https://github.com/python-greenlet/greenlet"
    url      = "https://pypi.io/packages/source/g/greenlet/greenlet-0.4.17.tar.gz"

    version('0.4.17', sha256='41d8835c69a78de718e466dd0e6bfd4b46125f21a67c3ff6d76d8d8059868d6b')
    version('0.4.13', sha256='0fef83d43bf87a5196c91e73cb9772f945a4caaff91242766c5916d1dd1381e4')

    depends_on('python', type=('build', 'link', 'run'))
