# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCligj(PythonPackage):
    """Click-based argument and option decorators for Python GIS command
    line programs"""

    homepage = "https://github.com/mapbox/cligj"
    url      = "https://github.com/mapbox/cligj/archive/0.5.0.zip"

    version('0.5.0', sha256='ad158722a3f512f7eb33526479acf5cb53d9e59ca15cd494556440839783f106')
    version('0.4.0', sha256='5a5eb903ea66a8ccd41765dd276d9d08a6285f21dd99d41425ef80030d740351')

    depends_on('py-setuptools', type='build')
    depends_on('py-click', type=('build', 'run'))
