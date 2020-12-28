# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlotly(PythonPackage):
    """An interactive, browser-based graphing library for Python"""

    homepage = "https://plot.ly/python/"
    url      = "https://pypi.io/packages/source/p/plotly/plotly-2.2.0.tar.gz"

    version('2.2.0', sha256='ca668911ffb4d11fed6d7fbb12236f8ecc6a7209db192326bcb64bdb41451a58')

    depends_on('py-setuptools', type='build')
    depends_on('py-decorator@4.0.6:', type=('build', 'run'))
    depends_on('py-nbformat@4.2.0:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
